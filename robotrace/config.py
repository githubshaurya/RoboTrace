from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(os.environ.get("ROBOTRACE_ROOT", Path.cwd())).resolve()
RESULTS_DIR = PROJECT_ROOT / "results"
REPORTS_DIR = PROJECT_ROOT / "reports"

def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def read_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write_json(path: str | Path, obj: Any, indent: int = 2) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=indent, default=str), encoding="utf-8")
    return path

def get_env_presence(name: str) -> dict:
    value = os.environ.get(name)
    return {"name": name, "present": isinstance(value, str) and len(value.strip()) > 0}
