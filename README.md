# RoboTrace

**Low-cost robustness and deployment-stress evaluation for VLA-style robot-learning traces.**

RoboTrace is a Kaggle-friendly research-engineering toolkit for evaluating how robot-learning and Vision-Language-Action-style traces behave under practical robustness and deployment failures. It focuses on action-trace stability, visual perturbation severity, symbolic instruction sensitivity, temporal/control-loop stress, and lightweight baseline evaluation without requiring paid APIs, robot hardware, or fragile robotics dependency installs.

The current release runs on `lerobot/pusht` and produces a complete evidence bundle: metrics, plots, reports, failure taxonomy, reproducibility notes, Hugging Face dataset artifacts, and a static dashboard.

---

## Why RoboTrace?

Most low-cost robotics/VLA projects either try to train a tiny model or run a narrow benchmark notebook. RoboTrace takes a different route.

It asks a practical systems question:

> Before deploying or even loading a heavy robot policy, can we stress-test recorded robot-learning traces for failures that appear in real deployment pipelines?

These failures include:

* delayed observations
* stale frames
* frame skipping
* action chunk reuse
* reduced inference/control frequency
* temporal jitter
* action horizon mismatch
* visual degradation
* symbolic instruction perturbations

The goal is not to claim real robot deployment. The goal is to build a reproducible evaluation scaffold that can expose where a robot-learning pipeline becomes unstable.

---

## Current release

The first public RoboTrace release evaluates PushT-style traces from `lerobot/pusht`.

### Completed pipeline

| Stage    | Purpose                                  | Output                                       |
| -------- | ---------------------------------------- | -------------------------------------------- |
| Stage 0  | Kaggle environment and token probe       | environment report                           |
| Stage 1  | Pure-Python repo skeleton and core tests | package, configs, tests                      |
| Stage 2  | Dataset discovery and schema probing     | dataset schema, previews                     |
| Stage 3  | Action trace metrics                     | smoothness, drift, magnitude, temporal stats |
| Stage 4  | Visual robustness suite                  | perturbation severity metrics and figures    |
| Stage 5  | Instruction sensitivity suite            | symbolic perturbation artifacts              |
| Stage 6  | Async deployment-stress simulator        | control/inference failure simulation         |
| Stage 7  | Optional baseline evaluation             | action-only sanity baselines                 |
| Stage 8  | Final report generation                  | reports, evidence index, limitations         |
| Stage 9  | Hugging Face release prep                | dataset card, Space app, release bundle      |
| Stage 10 | GitHub-ready packaging                   | tests, secret scan, source bundle            |

### Key result from the current run

In the async deployment-stress simulation, **action horizon mismatch** produced the highest-risk failure mode among the tested scenarios.

The highest-risk scenario was:

```text
mode: action_horizon_mismatch
params: {"actual_horizon": 8, "expected_horizon": 4}
```

This suggests that action/control-horizon assumptions can strongly distort recorded robot-learning traces, even before evaluating a learned policy on hardware.

---

## What RoboTrace evaluates

### 1. Dataset-level action trace behavior

RoboTrace computes metrics directly from dataset traces, without requiring a trained policy:

* action smoothness
* L1/L2 step deltas
* acceleration/jerk-like changes
* trajectory drift
* action magnitude distribution
* timestamp gaps and irregularity
* episode-level summaries
* trace visualizations

This makes the toolkit useful even when policy loading fails or robotics dependencies are unavailable.

### 2. Visual perturbation severity

RoboTrace applies deterministic image perturbations to real extracted dataset frames:

* brightness shift
* contrast shift
* blur
* JPEG compression
* random occlusion
* center crop
* resolution drop

The current release measures visual perturbation severity only. It does not claim image-conditioned policy robustness.

### 3. Instruction sensitivity artifacts

If language instructions are present, RoboTrace can generate deterministic perturbations such as shortening, masking, distractor insertion, and ambiguity injection.

For `lerobot/pusht`, the sampled rows did not expose natural-language instructions, so the current release uses symbolic fallback task perturbations. This is documented explicitly.

### 4. Async deployment-stress simulation

This is the main systems component.

RoboTrace simulates deployment-style failures over recorded action traces:

* frame skipping
* observation delay
* stale observation reuse
* action chunk reuse
* reduced inference frequency
* temporal jitter
* action horizon mismatch

It reports:

* mean action drift
* normalized drift
* smoothness degradation
* recovery-delay proxy
* chunk/control instability
* latency-quality tradeoff proxies
* risk scores by failure mode

### 5. Lightweight baseline evaluation

The current release includes action-only sanity baselines:

* replay/oracle baseline
* first-action hold
* mean-action baseline
* lagged-action baseline
* chunked-action variants
* smoothed action baseline

No real VLA policy is loaded in the current release. This is intentional: RoboTrace separates dataset analysis, baseline evaluation, and future real-policy evaluation instead of pretending all three are the same thing.

---

## Repository structure

```text
RoboTrace/
├── robotrace/                  # Core Python package
│   ├── metrics.py              # Trace-level metrics
│   ├── perturbations.py        # Visual perturbation utilities
│   ├── instruction_perturbations.py
│   ├── async_sim.py            # Deployment-stress simulator
│   ├── baselines.py            # Lightweight action baselines
│   ├── reporters.py
│   └── visualization.py
│
├── configs/                    # Dataset, metric, perturbation configs
├── tests/                      # CPU-safe unit tests
├── reports/                    # Final reports and limitations
├── results/
│   ├── summaries/              # CSV/JSON summaries
│   ├── figures/                # Generated plots
│   └── raw/                    # Raw JSONL/trace artifacts
│
├── artifacts/                  # Public evidence bundle
├── hf_release/                 # Hugging Face release assets
├── github_release/             # GitHub packaging and audit logs
└── case_studies/               # Stage-level run outputs
```

---

## Public artifacts

* Hugging Face Dataset: https://huggingface.co/datasets/i-am-shaurya05/robotrace-vla-robustness-traces
* Hugging Face Space: https://huggingface.co/spaces/i-am-shaurya05/robotrace-vla-dashboard

Edit these links if the repository namespace changes.

---

## Quick start

Clone the repository:

```bash
git clone https://github.com/githubshaurya/RoboTrace.git
cd RoboTrace
```

Install the package in editable mode:

```bash
pip install -e .
```

Run tests:

```bash
python -m pytest tests -q
```

Open the final report:

```bash
cat reports/robotrace_report.md
```

Inspect final metrics:

```bash
python - <<'PY'
import pandas as pd
df = pd.read_csv("results/summaries/robotrace_final_metrics.csv")
print(df.head(20))
PY
```

---

## Main outputs

The release contains:

```text
reports/robotrace_report.md
reports/limitations.md
reports/reproducibility.md
reports/failure_taxonomy.md

results/summaries/robotrace_final_metrics.csv
results/summaries/robotrace_final_summary.json
results/summaries/robotrace_evidence_index.csv

artifacts/reports/
artifacts/summaries/
artifacts/figures/

github_release/security/stage10_secret_scan.md
github_release/logs/stage10_test_log.txt
```

---

## Evidence discipline

RoboTrace is designed around saved evidence rather than loose claims.

The current release includes:

* raw stage summaries
* final metrics table
* evidence index
* generated figures
* report files
* limitations file
* reproducibility notes
* secret scan report
* test logs

Every major public claim should be traceable to a saved artifact.

---

## Limitations

RoboTrace does **not** claim:

* real robot hardware validation
* real VLA policy robustness
* natural-language instruction robustness for `lerobot/pusht`
* task success-rate degradation
* measured serving latency
* SOTA benchmark performance

The current run is an offline trace-level and simulation-level evaluation. It is meant to be a practical evaluation scaffold, not a replacement for hardware experiments or full policy benchmarking.

---

## Roadmap

Possible next extensions:

* add more LeRobot-style datasets
* add real-policy adapters in isolated optional stages
* support SmolVLA/LeRobot policy evaluation when environment compatibility allows
* add nearest-neighbor visual-action baseline
* add tiny behavior-cloning baseline
* add more deployment stress modes
* compare async stress sensitivity across datasets
* export report tables directly into paper-style LaTeX

---

## Citation

If you use RoboTrace, cite the repository or public artifact page.

```bibtex
@software{robotrace2026,
  title = {RoboTrace: Low-Cost Robustness and Deployment-Stress Evaluation for VLA-Style Robot-Learning Traces},
  author = {Shaurya Omar},
  year = {2026},
  url = {https://github.com/githubshaurya/RoboTrace}
}
```

---

## License

MIT License.
