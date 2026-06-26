from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
import numpy as np

def _flatten_obs(obs: Any) -> np.ndarray:
    arr = np.asarray(obs, dtype=np.float32)
    return arr.reshape(arr.shape[0], -1) if arr.ndim >= 2 else arr.reshape(-1, 1)

@dataclass
class ReplayPolicy:
    actions: Any

    def __post_init__(self) -> None:
        arr = np.asarray(self.actions, dtype=np.float32)
        if arr.ndim == 1:
            arr = arr.reshape(-1, 1)
        self.actions = arr

    def predict(self, step: int, observation: Optional[Any] = None, instruction: Optional[str] = None) -> np.ndarray:
        idx = int(np.clip(step, 0, self.actions.shape[0] - 1))
        return self.actions[idx].copy()

    def rollout(self, num_steps: Optional[int] = None) -> np.ndarray:
        n = self.actions.shape[0] if num_steps is None else int(num_steps)
        return np.stack([self.predict(i) for i in range(n)], axis=0)

@dataclass
class NearestNeighborActionBaseline:
    observations: Any
    actions: Any

    def __post_init__(self) -> None:
        self.obs_matrix = _flatten_obs(self.observations)
        self.action_matrix = np.asarray(self.actions, dtype=np.float32)
        if self.action_matrix.ndim == 1:
            self.action_matrix = self.action_matrix.reshape(-1, 1)
        if self.obs_matrix.shape[0] != self.action_matrix.shape[0]:
            raise ValueError("observations and actions must have same first dimension")

    def predict(self, observation: Any) -> np.ndarray:
        q = np.asarray(observation, dtype=np.float32).reshape(1, -1)
        if q.shape[1] != self.obs_matrix.shape[1]:
            raise ValueError(f"observation feature dim {q.shape[1]} != fitted dim {self.obs_matrix.shape[1]}")
        dist = np.sum((self.obs_matrix - q) ** 2, axis=1)
        return self.action_matrix[int(np.argmin(dist))].copy()
