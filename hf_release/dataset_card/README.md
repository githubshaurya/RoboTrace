---
license: mit
task_categories:
- robotics
- time-series-forecasting
- computer-vision
language:
- en
tags:
- robotics
- robot-learning
- vla
- robustness
- deployment-stress
- kaggle
- lerobot
- pusht
pretty_name: RoboTrace Evidence Bundle
---

# RoboTrace Evidence Bundle

RoboTrace is a no-paid-API, Kaggle-friendly robustness and deployment-stress evaluation toolkit for low-cost VLA-style robot-learning traces.

This release bundle contains reports, summary metrics, figures, and evidence indices from a staged RoboTrace run on `lerobot/pusht` split `train`.

## What this release includes

- Dataset probing evidence
- Action-trace metrics
- Visual perturbation severity analysis
- Instruction sensitivity artifacts
- Async deployment-stress simulation
- Lightweight action-only baseline evaluation
- Final report, limitations, reproducibility notes, and failure taxonomy

## Main finding

The strongest finding in this run is that **action horizon mismatch** was the highest-risk async deployment-stress mode.

- Top async mode by drift: `action_horizon_mismatch`
- Top async risk scenario: `{"actual_horizon": 8, "expected_horizon": 4}`
- Stage 7 top baseline by quality: `replay_oracle`
- Stage 7 worst baseline by risk: `first_action_hold`

## Important limitations

This release does **not** claim:

- real robot hardware validation
- real VLA policy robustness
- natural-language instruction robustness for `lerobot/pusht`
- task success-rate degradation
- measured serving latency
- SOTA benchmark status

The visual robustness stage perturbs real frames extracted from dataset repository video files, but no image-conditioned policy was evaluated. The instruction sensitivity stage found symbolic task labels only for this dataset sample.

## Files

Key files are under:

- `artifacts/reports/`
- `artifacts/summaries/`
- `artifacts/figures/`
- `manifest/release_manifest.json`

## Reproducibility

This run was designed for Kaggle execution with no paid APIs and no forced LeRobot installation. See `artifacts/reports/reproducibility.md`.

## Citation

If using this artifact, cite the repository or project page once published.
