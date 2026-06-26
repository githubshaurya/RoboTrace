from __future__ import annotations

from pathlib import Path
from typing import Any, Optional
import numpy as np

def save_action_plot(actions: Any, path: str | Path, title: Optional[str] = None) -> Path:
    import matplotlib.pyplot as plt
    arr = np.asarray(actions, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure()
    for dim in range(arr.shape[1]):
        plt.plot(arr[:, dim], label=f"dim_{dim}")
    plt.xlabel("step")
    plt.ylabel("action")
    if title:
        plt.title(title)
    if arr.shape[1] <= 8:
        plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path
