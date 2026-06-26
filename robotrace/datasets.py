from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import numpy as np
from .episode_schema import EpisodeTrace

@dataclass
class DatasetProbeResult:
    dataset_name: str
    status: str
    episodes: List[EpisodeTrace] = field(default_factory=list)
    schema: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "status": self.status,
            "num_episodes": len(self.episodes),
            "schema": self.schema,
            "warnings": list(self.warnings),
            "episodes": [ep.to_summary_dict() for ep in self.episodes],
        }

def make_synthetic_episode(num_steps: int = 16, action_dim: int = 4, episode_id: str = "synthetic_0") -> EpisodeTrace:
    t = np.linspace(0, 1, int(num_steps), dtype=np.float32)
    actions = []
    for d in range(int(action_dim)):
        actions.append(np.sin(2 * np.pi * (d + 1) * t) * (0.1 + 0.05 * d))
    arr = np.stack(actions, axis=1)
    timestamps = np.arange(num_steps, dtype=np.float64) / 10.0
    return EpisodeTrace(
        episode_id=episode_id,
        actions=arr,
        timestamps=timestamps,
        instruction="move the object to the target",
        metadata={"source": "synthetic"},
    )

def infer_array_schema(obj: Any) -> Dict[str, Any]:
    try:
        arr = np.asarray(obj)
        return {"shape": list(arr.shape), "dtype": str(arr.dtype), "ndim": int(arr.ndim)}
    except Exception as e:
        return {"error": repr(e)}
