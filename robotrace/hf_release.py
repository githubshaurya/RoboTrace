from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

def token_presence() -> Dict[str, bool]:
    return {"HF_TOKEN": bool(os.environ.get("HF_TOKEN")), "GITHUB_TOKEN": bool(os.environ.get("GITHUB_TOKEN"))}

def prepare_local_hf_dataset_folder(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
