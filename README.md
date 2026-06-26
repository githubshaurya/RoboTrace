# RoboTrace

**Low-cost deployment-stress evaluation for robot-learning and VLA-style inference pipelines.**

RoboTrace is a research-engineering toolkit for testing how recorded robot-learning traces behave under practical deployment failures: stale observations, frame skipping, reduced inference frequency, temporal jitter, action chunk reuse, visual degradation, symbolic instruction perturbations, and action-horizon mismatch.

It is designed for constrained environments such as Kaggle/Colab, where robot hardware, paid APIs, and heavy VLA policy execution may not be available.

---

## Problem

Robot and VLA systems are usually discussed through model quality or task success. In deployment, many failures also come from the inference/control pipeline itself:

* observations arrive late
* frames are skipped
* stale observations are reused
* control loops run slower than expected
* action chunks are reused incorrectly
* action horizons mismatch between policy assumptions and runtime execution
* visual input quality degrades
* task/instruction representations become noisy or incomplete

RoboTrace studies these failure modes using saved robot-learning traces before expensive hardware or full-policy evaluation.

---

## Objective

RoboTrace asks:

> Can we stress-test recorded robot-learning traces for edge/deployment-style inference failures before running a heavy VLA policy or robot hardware?

The goal is to produce reproducible engineering evidence under low-cost compute constraints.

---

## Current release

The first release evaluates:

```text
lerobot/pusht
```

Run summary:

| Item                     | Value |
| ------------------------ | ----: |
| Usable episodes          |     4 |
| Step metric rows         |   512 |
| Visual frames sampled    |    12 |
| Visual perturbation rows |   144 |
| Async stress scenarios   |    26 |
| Async simulation rows    |   104 |
| Baselines evaluated      |     8 |
| Baseline eval rows       |    32 |
| Real VLA policy loaded   | False |

---

## Main finding

The strongest deployment-stress failure mode in this run was:

```text
action_horizon_mismatch
```

Highest-risk scenario:

```text
mode: action_horizon_mismatch
params: {"actual_horizon": 8, "expected_horizon": 4}
risk_score_proxy: 2.5562635495893855
mean_l2_drift_mean: 138.2900505065918
```

This suggests that action/control-horizon assumptions can significantly distort recorded robot-learning traces even before a learned policy is deployed on hardware.

---

## Why this is relevant to inference and edge AI

RoboTrace is useful for evaluating failure modes around the **runtime layer** of embodied AI systems:

* edge inference frequency constraints
* control-loop degradation
* stale observation handling
* action chunk scheduling
* trace stability under delayed inputs
* deployment-time robustness before hardware testing
* lightweight evaluation when full VLA execution is unavailable

This makes the project relevant to:

* VLA / embodied AI evaluation
* robotics inference systems
* edge AI deployment
* multimodal AI robustness
* low-cost AI systems research
* reproducible research-engineering workflows

---

## What RoboTrace evaluates

### Action trace stability

* L1/L2 step deltas
* action smoothness
* trajectory drift
* action magnitude distribution
* timestamp gap statistics

### Visual robustness severity

* brightness
* contrast
* blur
* JPEG compression
* random occlusion
* center crop
* resolution drop

### Instruction sensitivity artifacts

* symbolic masking
* symbolic distractors
* symbolic ambiguity
* fallback handling when natural-language instructions are absent

### Async deployment-stress simulation

* frame skipping
* observation delay
* stale observation reuse
* action chunk reuse
* reduced inference frequency
* temporal jitter
* action-horizon mismatch

### Lightweight baselines

* replay/oracle
* first-action hold
* mean action
* lagged action
* chunked replay
* linear extrapolation

---

## Results

Read:

* [`RESULTS.md`](RESULTS.md)
* [`reports/robotrace_report.md`](reports/robotrace_report.md)

Key files:

```text
results/summaries/robotrace_final_metrics.csv
results/summaries/robotrace_final_summary.json
results/summaries/robotrace_evidence_index.csv
results/figures/
reports/
artifacts/
```

---

## Repository structure

```text
RoboTrace/
├── robotrace/             # Core package
├── tests/                 # CPU-safe tests
├── configs/               # Config files
├── reports/               # Final report and limitations
├── results/
│   ├── summaries/         # CSV/JSON metrics
│   └── figures/           # Plots
├── artifacts/             # Public evidence bundle
├── hf_release/            # Hugging Face release assets
└── case_studies/          # Stage outputs
```

---

## Public artifacts

* Hugging Face Dataset: https://huggingface.co/datasets/i-am-shaurya05/robotrace-vla-robustness-traces
* Hugging Face Space: https://huggingface.co/spaces/i-am-shaurya05/robotrace-vla-dashboard

---

## Quick start

```bash
git clone https://github.com/githubshaurya/RoboTrace.git
cd RoboTrace
pip install -e .
python -m pytest tests -q
```

Inspect metrics:

```bash
python - <<'PY'
import pandas as pd
df = pd.read_csv("results/summaries/robotrace_final_metrics.csv")
print(df.head(20))
PY
```

---

## Non-claims

RoboTrace does **not** claim:

* real robot hardware validation
* real VLA policy robustness
* natural-language instruction robustness for `lerobot/pusht`
* task success-rate degradation
* measured serving latency
* SOTA benchmark performance

The current release is an offline trace-level and simulation-level evaluation scaffold.

---

## License

MIT.
