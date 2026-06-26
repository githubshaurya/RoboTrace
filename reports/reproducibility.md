# RoboTrace Reproducibility

- Generated UTC: `2026-06-26T06:55:41.637266+00:00`

## Execution environment

- `overall_status`: `PASS`

## Stage order

- `stage0_env_probe`: `PASS`
- `stage1_core`: `present`
- `stage2_dataset_probe`: `PASS`
- `stage3_trace_metrics`: `PASS`
- `stage4_visual_robustness`: `PASS`
- `stage5_instruction_sensitivity`: `PASS`
- `stage6_async_simulation`: `PASS`
- `stage7_optional_policy_eval`: `PASS`

## Data and artifacts

- Evidence index CSV: `/kaggle/working/RoboTrace/results/summaries/robotrace_evidence_index.csv`
- Evidence index JSON: `/kaggle/working/RoboTrace/results/summaries/robotrace_evidence_index.json`
- Missing evidence manifest JSON: `/kaggle/working/RoboTrace/results/summaries/robotrace_missing_evidence_manifest.json`
- Final metrics CSV: `/kaggle/working/RoboTrace/results/summaries/robotrace_final_metrics.csv`

## Determinism

All perturbations and async simulations in the current staged notebooks are deterministic. No paid APIs or LLM APIs were used.