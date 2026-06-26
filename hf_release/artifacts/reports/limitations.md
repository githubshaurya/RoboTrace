# RoboTrace Limitations

- Generated UTC: `2026-06-26T06:55:41.636827+00:00`

## Hard limitations

- Do not claim real robot hardware validation.
- Do not claim real VLA policy robustness.
- Do not claim natural-language instruction robustness for `lerobot/pusht` from this run.
- Do not claim task success or success-rate degradation.
- Do not claim measured serving latency; Stage 6 latency values are proxies.
- Do not claim SOTA benchmark status.

## Dataset limitation

The current run uses `lerobot/pusht`. This is useful for action trace and deployment-stress evaluation, but it does not expose natural-language instructions in the sampled rows. Stage 5 therefore uses symbolic fallback perturbations only.

## Policy limitation

No real VLA policy was loaded. Stage 7 evaluated only lightweight action-only baselines. Any future real-policy evaluation should be isolated to avoid dependency instability.

## Visual limitation

Visual perturbations were applied to real extracted frames, but no image-conditioned model was evaluated. Stage 4 is visual severity analysis, not visual policy robustness.

## Deployment limitation

Stage 6 uses offline action-trace transformations. It is a useful proxy for deployment stress, but it is not real-time robot serving or hardware execution.