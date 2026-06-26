from __future__ import annotations

import importlib.util
import inspect
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def main() -> int:
    test_dir = Path(__file__).resolve().parent
    files = sorted(test_dir.glob("test_*.py"))
    passed = 0
    failed = 0
    for path in files:
        module = load_module(path)
        for name, fn in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith("test_"):
                continue
            try:
                fn()
                print(f"PASS {path.name}::{name}")
                passed += 1
            except Exception:
                print(f"FAIL {path.name}::{name}")
                traceback.print_exc()
                failed += 1
    print(f"TEST_SUMMARY passed={passed} failed={failed}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
