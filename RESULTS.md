# RoboTrace Results

This page summarizes the first public RoboTrace run on `lerobot/pusht`.

## Summary

| Item                     |           Value |
| ------------------------ | --------------: |
| Dataset                  | `lerobot/pusht` |
| Split                    |         `train` |
| Usable episodes          |             `4` |
| Step metric rows         |           `512` |
| Visual frames sampled    |            `12` |
| Visual perturbation rows |           `144` |
| Async stress scenarios   |            `26` |
| Async simulation rows    |           `104` |
| Baselines evaluated      |             `8` |
| Baseline eval rows       |            `32` |
| Real VLA policy loaded   |         `False` |

## Main conclusion

The strongest deployment-stress failure mode in this run was:

```text
action_horizon_mismatch
```

Highest-risk scenario:

```text
params: {"actual_horizon": 8, "expected_horizon": 4}
risk_score_proxy: 2.5562635495893855
mean_l2_drift_mean: 138.2900505065918
quality_score_proxy_mean: 0.727326073641731
```

## Inference / edge relevance

The result is relevant because action-horizon and control-frequency assumptions are runtime issues, not only model-quality issues.

In edge robotics or VLA deployment, the model may be correct in isolation but still fail when:

* observations arrive late
* inference runs slower than expected
* action chunks are reused for too long
* the policy assumes a different control horizon than the runtime
* visual inputs are degraded before reaching the policy

RoboTrace evaluates these issues using offline traces and lightweight simulations.

## Action trace metrics

| Metric                        |      Value |
| ----------------------------- | ---------: |
| Mean smoothness L2 step delta |   `8.2193` |
| Mean trajectory drift L2      | `181.0955` |
| Mean action magnitude L2      | `368.2736` |
| Mean episode length           |    `128.0` |

## Visual robustness

| Item                  |                Value |
| --------------------- | -------------------: |
| Image source          | `hf_repo_video_file` |
| Images sampled        |                 `12` |
| Perturbation rows     |                `144` |
| Policy drift measured |              `False` |

Visual perturbations measured severity only. No image-conditioned policy robustness is claimed.

## Instruction sensitivity

| Item                            |  Value |
| ------------------------------- | -----: |
| Raw instruction-like records    |  `512` |
| Natural-language unique records |    `0` |
| Symbolic fallback used          | `True` |
| Perturbation rows               |    `4` |

The dataset sample did not expose natural-language instructions, so the run used symbolic fallback perturbations.

## Async deployment-stress

Tested failure modes:

* frame skip
* observation delay
* stale observation
* action chunk reuse
* reduced inference frequency
* temporal jitter
* action-horizon mismatch

Top failure mode:

```text
action_horizon_mismatch
```

## Baseline evaluation

| Result                       | Value               |
| ---------------------------- | ------------------- |
| Best baseline by quality     | `replay_oracle`     |
| Worst baseline by risk       | `first_action_hold` |
| Worst baseline mean L2 drift | `183.9531`          |

## Evidence files

```text
reports/robotrace_report.md
reports/limitations.md
reports/reproducibility.md
reports/failure_taxonomy.md

results/summaries/robotrace_final_metrics.csv
results/summaries/robotrace_final_summary.json
results/summaries/robotrace_evidence_index.csv

results/figures/
artifacts/reports/
artifacts/summaries/
artifacts/figures/
```

## Interpretation

RoboTrace is strongest as a research-engineering artifact for low-cost robotics/VLA deployment evaluation.

It should not be presented as a real robot benchmark, real VLA policy benchmark, or measured edge-latency benchmark.
