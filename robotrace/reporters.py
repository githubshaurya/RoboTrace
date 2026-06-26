from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

def _json_default(obj):
    try:
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
    except Exception:
        pass
    return str(obj)

def write_json(path: str | Path, obj: Any) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=_json_default), encoding="utf-8")
    return path

def write_jsonl(path: str | Path, rows: Iterable[Dict[str, Any]]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, default=_json_default) + "\n")
    return path

def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    keys = sorted({key for row in rows for key in row.keys()})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path

def markdown_table(rows: List[Dict[str, Any]], max_rows: int = 20) -> str:
    if not rows:
        return "_No rows._"
    keys = list(rows[0].keys())
    lines = [
        "| " + " | ".join(keys) + " |",
        "| " + " | ".join(["---"] * len(keys)) + " |",
    ]
    for row in rows[:max_rows]:
        lines.append("| " + " | ".join(str(row.get(k, "")) for k in keys) + " |")
    if len(rows) > max_rows:
        lines.append(f"\n_Showing {max_rows} of {len(rows)} rows._")
    return "\n".join(lines)

def write_markdown_report(path: str | Path, title: str, sections: Dict[str, str]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    for name, body in sections.items():
        lines.extend([f"## {name}", "", body.strip(), ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
