from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

import numpy as np

@dataclass
class EpisodeTrace:
    episode_id: str
    actions: Any
    timestamps: Optional[Any] = None
    observations: Optional[Any] = None
    instruction: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        arr = np.asarray(self.actions, dtype=np.float32)
        if arr.ndim == 1:
            arr = arr.reshape(-1, 1)
        if arr.ndim != 2:
            raise ValueError(f"actions must be 1D or 2D, got shape {arr.shape}")
        if arr.shape[0] == 0:
            raise ValueError("episode must contain at least one action step")
        self.actions = arr
        self.num_steps = int(arr.shape[0])
        self.action_dim = int(arr.shape[1])
        if self.timestamps is not None:
            ts = np.asarray(self.timestamps, dtype=np.float64)
            if ts.ndim != 1:
                raise ValueError("timestamps must be 1D")
            if ts.shape[0] != self.num_steps:
                raise ValueError(f"timestamps length {ts.shape[0]} does not match actions length {self.num_steps}")
            self.timestamps = ts

    def to_summary_dict(self) -> Dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "num_steps": self.num_steps,
            "action_dim": self.action_dim,
            "has_timestamps": self.timestamps is not None,
            "has_observations": self.observations is not None,
            "has_instruction": self.instruction is not None,
            "instruction": self.instruction,
            "metadata": dict(self.metadata),
        }

@dataclass
class EpisodeBatch:
    episodes: List[EpisodeTrace]

    @classmethod
    def from_iterable(cls, episodes: Iterable[EpisodeTrace]) -> "EpisodeBatch":
        items = list(episodes)
        if not items:
            raise ValueError("EpisodeBatch requires at least one episode")
        return cls(items)

    def __len__(self) -> int:
        return len(self.episodes)

    def action_dims(self) -> List[int]:
        return [ep.action_dim for ep in self.episodes]

    def total_steps(self) -> int:
        return int(sum(ep.num_steps for ep in self.episodes))

    def to_summary_dict(self) -> Dict[str, Any]:
        return {
            "num_episodes": len(self.episodes),
            "total_steps": self.total_steps(),
            "action_dims": self.action_dims(),
            "episodes": [ep.to_summary_dict() for ep in self.episodes],
        }
