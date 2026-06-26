import json
import tempfile
from pathlib import Path
from robotrace.reporters import write_json, write_jsonl, write_csv, write_markdown_report

def test_report_writers_create_files():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        json_path = write_json(tmp / "data.json", {"a": 1})
        assert json_path.exists()
        assert json.loads(json_path.read_text())["a"] == 1
        jsonl_path = write_jsonl(tmp / "data.jsonl", [{"a": 1}, {"a": 2}])
        assert jsonl_path.exists()
        assert len(jsonl_path.read_text().strip().splitlines()) == 2
        csv_path = write_csv(tmp / "data.csv", [{"a": 1, "b": 2}])
        assert csv_path.exists()
        assert "a,b" in csv_path.read_text() or "b,a" in csv_path.read_text()
        md_path = write_markdown_report(tmp / "report.md", "Demo", {"Section": "Body"})
        assert md_path.exists()
        assert "# Demo" in md_path.read_text()
