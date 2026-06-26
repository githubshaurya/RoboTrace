from __future__ import annotations

from typing import Any, Dict, List
import numpy as np
from .async_sim import simulate_async_suite
from .metrics import action_trace_distance, episode_metrics

def evaluate_action_trace(reference_actions: Any, candidate_actions: Any) -> Dict[str, Any]:
    return {
        "distance": action_trace_distance(reference_actions, candidate_actions),
        "reference_metrics": episode_metrics(reference_actions),
        "candidate_metrics": episode_metrics(candidate_actions),
    }

def evaluate_async_stress(reference_actions: Any) -> List[Dict[str, Any]]:
    return [result.to_dict() for result in simulate_async_suite(reference_actions)]

def rollout_replay_policy(policy: Any, num_steps: int) -> np.ndarray:
    actions = []
    for i in range(int(num_steps)):
        actions.append(policy.predict(i))
    return np.asarray(actions, dtype=np.float32)
