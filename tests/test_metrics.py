import math
import numpy as np
from robotrace.episode_schema import EpisodeTrace, EpisodeBatch
from robotrace.metrics import episode_metrics, action_trace_distance, summarize_episode_metrics

def test_episode_trace_schema():
    actions = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float32)
    ep = EpisodeTrace("ep0", actions, timestamps=[0.0, 0.1, 0.2], instruction="move the block")
    assert ep.num_steps == 3
    assert ep.action_dim == 2
    assert ep.to_summary_dict()["has_instruction"] is True
    batch = EpisodeBatch.from_iterable([ep])
    assert len(batch) == 1
    assert batch.total_steps() == 3

def test_episode_metrics_basic_values():
    actions = np.array([[0, 0], [1, 0], [1, 1]], dtype=np.float32)
    metrics = episode_metrics(actions, timestamps=[0.0, 0.1, 0.2], episode_id="ep0")
    assert metrics["num_steps"] == 3
    assert metrics["action_dim"] == 2
    assert abs(metrics["trajectory_drift_l2"] - math.sqrt(2)) < 1e-5
    assert abs(metrics["trajectory_path_l2"] - 2.0) < 1e-5
    assert metrics["has_timestamps"] is True
    assert abs(metrics["timestamp_gap_mean"] - 0.1) < 1e-8

def test_action_trace_distance():
    ref = np.zeros((4, 2), dtype=np.float32)
    cand = np.ones((4, 2), dtype=np.float32)
    dist = action_trace_distance(ref, cand)
    assert dist["aligned_steps"] == 4
    assert dist["aligned_dims"] == 2
    assert abs(dist["mean_l2_drift"] - math.sqrt(2)) < 1e-5

def test_summarize_episode_metrics():
    a = episode_metrics(np.zeros((3, 2)))
    b = episode_metrics(np.ones((4, 2)))
    summary = summarize_episode_metrics([a, b])
    assert summary["num_episodes"] == 2
    assert "num_steps_mean" in summary
    assert summary["num_steps_min"] == 3
    assert summary["num_steps_max"] == 4
