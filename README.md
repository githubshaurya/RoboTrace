# RoboTrace

**RoboTrace is a Kaggle-friendly robustness and deployment-stress evaluation toolkit for VLA-style robot-learning traces.**

It evaluates how recorded robot-learning traces behave under practical failure modes: action instability, visual degradation, symbolic instruction perturbations, temporal jitter, stale observations, frame skipping, reduced inference/control frequency, action chunk reuse, and action-horizon mismatch.

The first public release runs on `lerobot/pusht` and produces an evidence bundle with metrics, plots, reports, failure analysis, Hugging Face dataset artifacts, and a dashboard.

---

## Problem

Vision-Language-Action and robot-learning systems are usually evaluated through policy performance or hardware trials. Those are expensive, fragile, and often impossible on free compute.

RoboTrace focuses on an earlier systems question:

> Before loading a heavy VLA policy or running hardware, can we stress-test recorded robot-learning traces for deployment-style failures?

This matters because real embodied-AI deployments often fail due to timing, control-loop assumptions, observation delays, action-horizon mismatch, and data robustness issues, not only model accuracy.

---

## Objective

RoboTrace aims to provide a low-cost evaluation scaffold that works even when:

* no robot hardware is available
* no paid API is available
* LeRobot/policy loading fails
* only Kaggle/Colab-style compute is available
* the user needs reproducible evidence, not just a demo notebook

---

## Current release

Dataset:

```text
lerobot/pusht
```

Current run summary:

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

The strongest result from the current run is that **action-horizon mismatch** produced the highest deployment-stress risk.

Highest-risk async scenario:

```text
mode: action_horizon_mismatch
params: {"actual_horizon": 8, "expected_horizon": 4}
risk_score_proxy: 2.5562635495893855
mean_l2_drift_mean: 138.2900505065918
```

This suggests that action/control-horizon assumptions can strongly distort robot-learning traces even before policy deployment or hardware execution.

---

## What RoboTrace evaluates

### 1. Action trace metrics

* action smoothness
* L1/L2 step deltas
* trajectory drift
* action magnitude distribution
* timestamp gaps
* episode-level summaries

### 2. Visual perturbation severity

* brightness
* contrast
* blur
* JPEG compression
* random occlusion
* center crop
* resolution drop

### 3. Instruction sensitivity artifacts

* symbolic masking
* symbolic distractors
* symbolic ambiguity
* fallback handling when natural-language instructions are absent

### 4. Async deployment-stress simulation

* frame skipping
* observation delay
* stale observation reuse
* action chunk reuse
* reduced inference frequency
* temporal jitter
* action horizon mismatch

### 5. Lightweight baselines

* replay/oracle baseline
* first-action hold
* mean-action baseline
* lagged-action baseline
* chunked-action replay
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
├── hf_release/            # HF release assets
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

## Roadmap

* add more LeRobot-style datasets
* add isolated real-policy adapters
* add nearest-neighbor visual-action baseline
* add tiny behavior-cloning baseline
* compare async stress sensitivity across datasets
* export paper-style tables

---

## Citation

```bibtex
@software{robotrace2026,
  title = {RoboTrace: Low-Cost Robustness and Deployment-Stress Evaluation for VLA-Style Robot-Learning Traces},
  author = {Shaurya Omar},
  year = {2026},
  url = {https://github.com/githubshaurya/RoboTrace}
}
```

## License

MIT.
