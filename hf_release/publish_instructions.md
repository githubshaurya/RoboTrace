# RoboTrace Publish Instructions

Generated UTC: `2026-06-26T06:55:53.037815+00:00`

This notebook intentionally does **not** push anything.

## What to upload

### Hugging Face Dataset-style evidence bundle

Upload the folder:

```text
/kaggle/working/RoboTrace/hf_release
```

The dataset card is at:

```text
/kaggle/working/RoboTrace/hf_release/dataset_card/README.md
```

### Hugging Face Space static viewer

Upload the folder:

```text
/kaggle/working/RoboTrace/hf_release/space_app
```

The Space app includes its own local `artifacts/` copy.

## GitHub repository prep

Before pushing to GitHub:

1. Keep source code:
   - `robotrace/`
   - `configs/`
   - `tests/`
   - `reports/`
   - selected notebooks
   - `hf_release/manifest/`
2. Avoid committing huge raw artifacts unless intentionally using Git LFS.
3. Commit curated summary outputs and figures.
4. Keep tokens out of git. Do not paste `HF_TOKEN` or `GITHUB_TOKEN`.

## Suggested GitHub commit message

```text
Add RoboTrace staged evaluation pipeline and evidence reports
```

## Suggested repository description

```text
Kaggle-friendly robustness and deployment-stress evaluation toolkit for low-cost VLA-style robot-learning traces.
```

## Safe claims

- Kaggle-friendly staged evaluation
- no paid APIs
- no required LeRobot install for this run
- action-trace metrics
- visual perturbation severity
- symbolic instruction sensitivity artifact
- async deployment-stress simulator
- action-only sanity baselines

## Claims to avoid

- real robot hardware validation
- real VLA policy robustness
- natural-language instruction robustness for `lerobot/pusht`
- task success rate degradation
- measured serving latency
- SOTA benchmark status
