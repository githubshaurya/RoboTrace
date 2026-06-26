# RoboTrace Public Claims

Generated UTC: `2026-06-26T06:56:08.570765+00:00`

## Safe claims

- RoboTrace is a Kaggle-friendly staged evaluation toolkit.
- RoboTrace uses no paid APIs in the current pipeline.
- The current run evaluates `lerobot/pusht` without requiring LeRobot installation.
- The pipeline computes dataset-level action trace metrics.
- The pipeline applies visual perturbations to real extracted dataset frames.
- The pipeline records that `lerobot/pusht` exposes symbolic task labels only in the sampled rows.
- The async simulator identifies action horizon mismatch as the highest-risk deployment-stress mode in this run.
- Stage 7 includes action-only sanity baselines.

## Do not claim

- real robot hardware validation
- real VLA policy robustness
- natural-language instruction robustness for `lerobot/pusht`
- task success-rate degradation
- measured serving latency
- SOTA benchmark status

## One-line positioning

RoboTrace is a low-cost robustness and deployment-stress evaluation scaffold for VLA-style robot-learning traces, designed to run reproducibly in Kaggle.
