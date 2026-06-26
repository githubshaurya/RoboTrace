
import json
from pathlib import Path

import gradio as gr
import pandas as pd

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"

def read_text(path, fallback="File not found."):
    try:
        path = Path(path)
        if path.exists():
            return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"
    return fallback

def read_json(path):
    try:
        path = Path(path)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {}

def read_csv(path):
    try:
        path = Path(path)
        if path.exists():
            return pd.read_csv(path)
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})
    return pd.DataFrame({"status": ["File not found"]})

summary = read_json(ARTIFACTS / "summaries" / "robotrace_final_summary.json")
report_md = read_text(ARTIFACTS / "reports" / "robotrace_report.md")
limitations_md = read_text(ARTIFACTS / "reports" / "limitations.md")
repro_md = read_text(ARTIFACTS / "reports" / "reproducibility.md")

metrics_df = read_csv(ARTIFACTS / "summaries" / "robotrace_final_metrics.csv")
async_df = read_csv(ARTIFACTS / "summaries" / "async_summary.csv")
baseline_df = read_csv(ARTIFACTS / "summaries" / "stage7_baseline_summary.csv")
visual_df = read_csv(ARTIFACTS / "summaries" / "stage4_visual_summary.csv")

def overview():
    core = summary.get("core_findings", {})
    lines = [
        "# RoboTrace Evidence Viewer",
        "",
        f"**Dataset:** `{summary.get('dataset', 'unknown')}`",
        f"**Split:** `{summary.get('split', 'unknown')}`",
        f"**Completed stages:** `{summary.get('completed_stage_count', 'unknown')}`",
        f"**Evidence indexed:** `{summary.get('evidence_indexed', summary.get('evidence_count', 'unknown'))}`",
        "",
        "## Core findings",
        "",
        f"- Stage 6 top mode by drift: `{core.get('stage6_top_mode_by_drift')}`",
        f"- Stage 7 top baseline by quality: `{core.get('stage7_top_baseline_by_quality')}`",
        f"- Stage 7 worst baseline by risk: `{core.get('stage7_worst_baseline_by_risk')}`",
        f"- Stage 5 symbolic fallback used: `{core.get('stage5_symbolic_fallback_used')}`",
        f"- Stage 4 image source: `{core.get('stage4_image_source')}`",
        "",
        "This app is a static viewer. It does not run robot policies, call APIs, or evaluate hardware.",
    ]
    return "\n".join(lines)

with gr.Blocks(title="RoboTrace Evidence Viewer") as demo:
    gr.Markdown(overview())

    with gr.Tab("Final Report"):
        gr.Markdown(report_md)

    with gr.Tab("Final Metrics"):
        gr.Dataframe(metrics_df, interactive=False)

    with gr.Tab("Async Stress Summary"):
        gr.Dataframe(async_df, interactive=False)

    with gr.Tab("Baseline Summary"):
        gr.Dataframe(baseline_df, interactive=False)

    with gr.Tab("Visual Summary"):
        gr.Dataframe(visual_df, interactive=False)

    with gr.Tab("Limitations"):
        gr.Markdown(limitations_md)

    with gr.Tab("Reproducibility"):
        gr.Markdown(repro_md)

if __name__ == "__main__":
    demo.launch()
