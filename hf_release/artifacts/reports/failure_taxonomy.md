# RoboTrace Failure Taxonomy

- Generated UTC: `2026-06-26T06:55:41.637971+00:00`

## Dataset/schema failures

- Dataset inaccessible or missing split
- Missing action field
- Missing timestamp field
- Visual observations stored as videos instead of decoded row images
- Natural-language instructions absent, requiring symbolic fallback

## Visual robustness failures

- Brightness shift
- Contrast shift
- Blur/detail loss
- Compression/quantization artifact
- Occlusion
- Crop/scale mismatch
- Resolution drop

## Deployment-stress failures

- Frame skip
- Observation delay
- Stale observation
- Action chunk reuse
- Reduced inference frequency
- Temporal jitter
- Action horizon mismatch

## Baseline/policy failures

- Constant action collapse
- First-action hold collapse
- One-step lag
- Bad extrapolation
- Chunk boundary discontinuity
- Real policy unavailable due to dependency risk

## Evidence from current run

The highest-risk async failure in the current run was action horizon mismatch. The worst action-only baseline was first-action hold.