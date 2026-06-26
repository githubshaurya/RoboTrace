from __future__ import annotations

from typing import Any, Dict, Iterable, Optional
import numpy as np

def _as_actions(actions: Any) -> np.ndarray:
    arr = np.asarray(actions, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    if arr.ndim != 2:
        raise ValueError(f"actions must be 1D or 2D, got shape {arr.shape}")
    if arr.shape[0] == 0:
        raise ValueError("actions must contain at least one step")
    return arr

def _safe_stats(values: Any, prefix: str) -> Dict[str, float]:
    arr = np.asarray(values, dtype=np.float64).reshape(-1)
    if arr.size == 0:
        return {
            f"{prefix}_mean": 0.0,
            f"{prefix}_std": 0.0,
            f"{prefix}_min": 0.0,
            f"{prefix}_max": 0.0,
            f"{prefix}_p50": 0.0,
            f"{prefix}_p90": 0.0,
        }
    return {
        f"{prefix}_mean": float(np.mean(arr)),
        f"{prefix}_std": float(np.std(arr)),
        f"{prefix}_min": float(np.min(arr)),
        f"{prefix}_max": float(np.max(arr)),
        f"{prefix}_p50": float(np.percentile(arr, 50)),
        f"{prefix}_p90": float(np.percentile(arr, 90)),
    }

def action_step_deltas(actions: Any) -> Dict[str, np.ndarray]:
    arr = _as_actions(actions)
    if arr.shape[0] < 2:
        zeros = np.zeros((0,), dtype=np.float32)
        return {"l1": zeros, "l2": zeros, "per_dim": np.zeros((0, arr.shape[1]), dtype=np.float32)}
    delta = np.diff(arr, axis=0)
    return {"l1": np.sum(np.abs(delta), axis=1), "l2": np.linalg.norm(delta, axis=1), "per_dim": delta}

def acceleration_like(actions: Any) -> np.ndarray:
    arr = _as_actions(actions)
    return np.zeros((0, arr.shape[1]), dtype=np.float32) if arr.shape[0] < 3 else np.diff(arr, n=2, axis=0)

def jerk_like(actions: Any) -> np.ndarray:
    arr = _as_actions(actions)
    return np.zeros((0, arr.shape[1]), dtype=np.float32) if arr.shape[0] < 4 else np.diff(arr, n=3, axis=0)

def trajectory_drift(actions: Any) -> Dict[str, float]:
    arr = _as_actions(actions)
    final_minus_start = arr[-1] - arr[0]
    step_l2 = action_step_deltas(arr)["l2"]
    cumulative_path = float(np.sum(step_l2)) if step_l2.size else 0.0
    final_drift = float(np.linalg.norm(final_minus_start))
    ratio = final_drift / cumulative_path if cumulative_path > 1e-12 else 0.0
    return {
        "trajectory_drift_l2": final_drift,
        "trajectory_path_l2": cumulative_path,
        "trajectory_directness_ratio": float(ratio),
    }

def action_magnitude_stats(actions: Any) -> Dict[str, float]:
    arr = _as_actions(actions)
    mags = np.linalg.norm(arr, axis=1)
    out = _safe_stats(mags, "action_magnitude_l2")
    out["action_abs_mean"] = float(np.mean(np.abs(arr)))
    out["action_abs_max"] = float(np.max(np.abs(arr)))
    return out

def gripper_distribution(actions: Any, gripper_dim: int = -1, threshold: float = 0.5) -> Dict[str, float]:
    arr = _as_actions(actions)
    dim = gripper_dim if gripper_dim >= 0 else arr.shape[1] + gripper_dim
    if dim < 0 or dim >= arr.shape[1]:
        return {}
    g = arr[:, dim]
    transitions = int(np.sum((g[1:] > threshold) != (g[:-1] > threshold))) if g.shape[0] >= 2 else 0
    return {
        "gripper_dim": int(dim),
        "gripper_mean": float(np.mean(g)),
        "gripper_min": float(np.min(g)),
        "gripper_max": float(np.max(g)),
        "gripper_open_fraction": float(np.mean(g > threshold)),
        "gripper_closed_fraction": float(np.mean(g <= threshold)),
        "gripper_transition_count": transitions,
    }

def timestamp_gap_stats(timestamps: Optional[Any]) -> Dict[str, float]:
    if timestamps is None:
        return {
            "has_timestamps": False,
            "timestamp_gap_mean": 0.0,
            "timestamp_gap_std": 0.0,
            "timestamp_gap_min": 0.0,
            "timestamp_gap_max": 0.0,
            "timestamp_irregularity": 0.0,
        }
    ts = np.asarray(timestamps, dtype=np.float64)
    if ts.ndim != 1:
        raise ValueError("timestamps must be 1D")
    if ts.size < 2:
        return {
            "has_timestamps": True,
            "timestamp_gap_mean": 0.0,
            "timestamp_gap_std": 0.0,
            "timestamp_gap_min": 0.0,
            "timestamp_gap_max": 0.0,
            "timestamp_irregularity": 0.0,
        }
    gaps = np.diff(ts)
    mean_gap = float(np.mean(gaps))
    std_gap = float(np.std(gaps))
    return {
        "has_timestamps": True,
        "timestamp_gap_mean": mean_gap,
        "timestamp_gap_std": std_gap,
        "timestamp_gap_min": float(np.min(gaps)),
        "timestamp_gap_max": float(np.max(gaps)),
        "timestamp_irregularity": float(std_gap / abs(mean_gap)) if abs(mean_gap) > 1e-12 else 0.0,
    }

def action_trace_distance(reference: Any, candidate: Any) -> Dict[str, float]:
    ref = _as_actions(reference)
    cand = _as_actions(candidate)
    n = min(ref.shape[0], cand.shape[0])
    d = min(ref.shape[1], cand.shape[1])
    if n == 0 or d == 0:
        return {
            "aligned_steps": 0,
            "aligned_dims": 0,
            "mean_l2_drift": 0.0,
            "max_l2_drift": 0.0,
            "final_l2_drift": 0.0,
            "missing_steps": max(0, ref.shape[0] - cand.shape[0]),
            "extra_steps": max(0, cand.shape[0] - ref.shape[0]),
        }
    diff = cand[:n, :d] - ref[:n, :d]
    l2 = np.linalg.norm(diff, axis=1)
    return {
        "aligned_steps": int(n),
        "aligned_dims": int(d),
        "mean_l2_drift": float(np.mean(l2)),
        "max_l2_drift": float(np.max(l2)),
        "final_l2_drift": float(l2[-1]),
        "missing_steps": int(max(0, ref.shape[0] - cand.shape[0])),
        "extra_steps": int(max(0, cand.shape[0] - ref.shape[0])),
    }

def episode_metrics(actions: Any, timestamps: Optional[Any] = None, episode_id: Optional[str] = None, gripper_dim: int = -1) -> Dict[str, float]:
    arr = _as_actions(actions)
    deltas = action_step_deltas(arr)
    acc = acceleration_like(arr)
    jerk = jerk_like(arr)
    out: Dict[str, float] = {"episode_id": episode_id or "", "num_steps": int(arr.shape[0]), "action_dim": int(arr.shape[1])}
    out.update(_safe_stats(deltas["l1"], "l1_step_delta"))
    out.update(_safe_stats(deltas["l2"], "l2_step_delta"))
    out.update(_safe_stats(np.linalg.norm(acc, axis=1) if acc.size else [], "acceleration_l2"))
    out.update(_safe_stats(np.linalg.norm(jerk, axis=1) if jerk.size else [], "jerk_l2"))
    out["smoothness_mean_l2_step_delta"] = out["l2_step_delta_mean"]
    out["smoothness_max_l2_step_delta"] = out["l2_step_delta_max"]
    out.update(trajectory_drift(arr))
    out.update(action_magnitude_stats(arr))
    out.update(gripper_distribution(arr, gripper_dim=gripper_dim))
    out.update(timestamp_gap_stats(timestamps))
    return out

def summarize_episode_metrics(rows: Iterable[Dict[str, Any]]) -> Dict[str, float]:
    items = list(rows)
    if not items:
        return {"num_episodes": 0}
    numeric_keys = [k for k, v in items[0].items() if isinstance(v, (int, float, np.integer, np.floating, bool))]
    summary: Dict[str, float] = {"num_episodes": int(len(items))}
    for key in numeric_keys:
        values = [float(row[key]) for row in items if key in row and isinstance(row[key], (int, float, np.integer, np.floating, bool))]
        if values:
            arr = np.asarray(values, dtype=np.float64)
            summary[f"{key}_mean"] = float(np.mean(arr))
            summary[f"{key}_min"] = float(np.min(arr))
            summary[f"{key}_max"] = float(np.max(arr))
    return summary
