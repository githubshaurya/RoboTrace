# RoboTrace Release Notes

Generated UTC: `2026-06-26T06:55:53.037461+00:00`

## Release contents

This release was generated from a staged Kaggle run over `lerobot/pusht` split `train`.

Included:

- final report
- public summary
- limitations
- reproducibility notes
- failure taxonomy
- final metrics
- evidence index
- selected figures
- static Hugging Face Space app
- dataset card

## Core findings

- Stage 6 top mode by drift: `action_horizon_mismatch`
- Stage 6 top risk scenario: `{"actual_horizon": 8, "expected_horizon": 4}`
- Stage 7 top baseline by quality: `replay_oracle`
- Stage 7 worst baseline by risk: `first_action_hold`
- Stage 5 symbolic fallback used: `True`
- Stage 4 image source: `hf_repo_video_file`

## Release stance

This is an evidence bundle and static viewer, not a claim of hardware performance or real VLA policy robustness.
