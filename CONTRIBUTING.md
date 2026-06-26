# Contributing to RoboTrace

RoboTrace contributions should preserve the staged, Kaggle-safe design.

## Rules

- Do not require paid APIs.
- Do not print tokens.
- Do not force CUDA/PyTorch reinstallations.
- Keep heavy dependency experiments isolated in separate stages.
- Prefer deterministic, testable metrics.
- Avoid overclaiming policy or hardware performance.

## Useful contribution types

- new dataset schema adapters
- new perturbation modes
- new async/deployment stress modes
- better report generation
- optional isolated policy adapters
- tests and documentation tied to behavior
