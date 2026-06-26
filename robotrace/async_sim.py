from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List
import numpy as np
from .metrics import action_trace_distance, episode_metrics

@dataclass
class AsyncSimulationResult:
    name: str
    actions: np.ndarray
    metadata: Dict[str, Any]
    metrics: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "metadata": dict(self.metadata),
            "metrics": dict(self.metrics),
            "num_steps": int(self.actions.shape[0]),
            "action_dim": int(self.actions.shape[1]) if self.actions.ndim == 2 else 0,
        }

def _as_actions(actions: Any) -> np.ndarray:
    arr = np.asarray(actions, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    if arr.ndim != 2:
        raise ValueError(f"actions must be 1D or 2D, got shape {arr.shape}")
    if arr.shape[0] == 0:
        raise ValueError("actions must contain at least one step")
    return arr

def _with_metrics(name: str, reference: np.ndarray, candidate: np.ndarray, metadata: Dict[str, Any]) -> AsyncSimulationResult:
    drift = action_trace_distance(reference, candidate)
    ref_metrics = episode_metrics(reference)
    cand_metrics = episode_metrics(candidate)
    ref_smooth = ref_metrics.get("smoothness_mean_l2_step_delta", 0.0)
    cand_smooth = cand_metrics.get("smoothness_mean_l2_step_delta", 0.0)
    metrics = {
        **drift,
        "reference_smoothness": float(ref_smooth),
        "candidate_smoothness": float(cand_smooth),
        "smoothness_degradation": float(cand_smooth - ref_smooth),
    }
    return AsyncSimulationResult(name=name, actions=candidate.astype(np.float32), metadata=metadata, metrics=metrics)

def simulate_frame_skip(actions: Any, skip: int = 2) -> AsyncSimulationResult:
    ref = _as_actions(actions)
    skip = max(1, int(skip))
    idx = (np.arange(ref.shape[0]) // skip) * skip
    idx = np.clip(idx, 0, ref.shape[0] - 1)
    return _with_metrics("frame_skip", ref, ref[idx], {"skip": skip})

def simulate_observation_delay(actions: Any, delay_steps: int = 2) -> AsyncSimulationResult:
    ref = _as_actions(actions)
    delay_steps = max(0, int(delay_steps))
    idx = np.maximum(0, np.arange(ref.shape[0]) - delay_steps)
    return _with_metrics("observation_delay", ref, ref[idx], {"delay_steps": delay_steps})

def simulate_stale_observation(actions: Any, stale_every: int = 3) -> AsyncSimulationResult:
    ref = _as_actions(actions)
    stale_every = max(1, int(stale_every))
    cand = ref.copy()
    for t in range(1, ref.shape[0]):
        if t % stale_every == 0:
            cand[t] = cand[t - 1]
    return _with_metrics("stale_observation", ref, cand, {"stale_every": stale_every})

def simulate_action_chunk_reuse(actions: Any, chunk_size: int = 4) -> AsyncSimulationResult:
    ref = _as_actions(actions)
    chunk_size = max(1, int(chunk_size))
    cand = ref.copy()
    for start in range(0, ref.shape[0], chunk_size):
        end = min(ref.shape[0], start + chunk_size)
        cand[start:end] = ref[start]
    result = _with_metrics("action_chunk_reuse", ref, cand, {"chunk_size": chunk_size})
    if ref.shape[0] > chunk_size:
        jumps = [float(np.linalg.norm(cand[b] - cand[b - 1])) for b in range(chunk_size, ref.shape[0], chunk_size)]
        result.metrics["chunk_boundary_discontinuity_mean"] = float(np.mean(jumps)) if jumps else 0.0
        result.metrics["chunk_boundary_discontinuity_max"] = float(np.max(jumps)) if jumps else 0.0
    else:
        result.metrics["chunk_boundary_discontinuity_mean"] = 0.0
        result.metrics["chunk_boundary_discontinuity_max"] = 0.0
    return result

def simulate_reduced_inference_frequency(actions: Any, frequency_divisor: int = 4) -> AsyncSimulationResult:
    ref = _as_actions(actions)
    frequency_divisor = max(1, int(frequency_divisor))
    idx = (np.arange(ref.shape[0]) // frequency_divisor) * frequency_divisor
    idx = np.clip(idx, 0, ref.shape[0] - 1)
    return _with_metrics("reduced_inference_frequency", ref, ref[idx], {"frequency_divisor": frequency_divisor})

def simulate_temporal_jitter(actions: Any, max_jitter_steps: int = 1) -> AsyncSimulationResult:
    ref = _as_actions(actions)
    max_jitter_steps = max(0, int(max_jitter_steps))
    if max_jitter_steps == 0:
        cand = ref.copy()
    else:
        offsets = ((np.arange(ref.shape[0]) % (2 * max_jitter_steps + 1)) - max_jitter_steps)
        idx = np.clip(np.arange(ref.shape[0]) + offsets, 0, ref.shape[0] - 1)
        cand = ref[idx]
    return _with_metrics("temporal_jitter", ref, cand, {"max_jitter_steps": max_jitter_steps})

def simulate_action_horizon_mismatch(actions: Any, expected_horizon: int = 4, actual_horizon: int = 2) -> AsyncSimulationResult:
    ref = _as_actions(actions)
    expected_horizon = max(1, int(expected_horizon))
    actual_horizon = max(1, int(actual_horizon))
    cand = ref.copy()
    write = 0
    read = 0
    while write < ref.shape[0]:
        source = ref[min(read, ref.shape[0] - 1)]
        end = min(ref.shape[0], write + actual_horizon)
        cand[write:end] = source
        write += actual_horizon
        read += expected_horizon
    return _with_metrics("action_horizon_mismatch", ref, cand, {"expected_horizon": expected_horizon, "actual_horizon": actual_horizon})

def recovery_delay_proxy(reference: Any, candidate: Any, tolerance: float = 0.05) -> int:
    ref = _as_actions(reference)
    cand = _as_actions(candidate)
    n = min(ref.shape[0], cand.shape[0])
    if n == 0:
        return 0
    l2 = np.linalg.norm(cand[:n] - ref[:n], axis=1)
    bad = l2 > float(tolerance)
    if not np.any(bad):
        return 0
    return int(max(0, int(np.max(np.where(bad)[0]))))

def simulate_async_suite(actions: Any) -> List[AsyncSimulationResult]:
    ref = _as_actions(actions)
    results = [
        simulate_frame_skip(ref, skip=2),
        simulate_observation_delay(ref, delay_steps=2),
        simulate_stale_observation(ref, stale_every=3),
        simulate_action_chunk_reuse(ref, chunk_size=4),
        simulate_reduced_inference_frequency(ref, frequency_divisor=4),
        simulate_temporal_jitter(ref, max_jitter_steps=1),
        simulate_action_horizon_mismatch(ref, expected_horizon=4, actual_horizon=2),
    ]
    for result in results:
        result.metrics["recovery_delay_proxy"] = recovery_delay_proxy(ref, result.actions)
    return results
