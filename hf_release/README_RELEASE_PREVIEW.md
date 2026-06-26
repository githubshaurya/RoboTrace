# RoboTrace Public Summary

RoboTrace is a no-paid-API, Kaggle-friendly robustness and deployment-stress evaluation toolkit for low-cost VLA-style robot-learning traces.

In this run, RoboTrace evaluated `lerobot/pusht` without requiring LeRobot installation. It produced dataset probes, action-trace metrics, visual perturbation severity metrics, symbolic instruction perturbation artifacts, async deployment-stress simulations, and lightweight action-only baseline evaluations.

The main finding is that action horizon mismatch produced the highest deployment-stress risk in the offline action-trace simulator.

Important limitation: this run does not evaluate a real VLA policy or hardware robot. It is an evaluation and stress-testing scaffold, not a hardware benchmark.