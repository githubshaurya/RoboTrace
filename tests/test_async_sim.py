import numpy as np
from robotrace.async_sim import simulate_action_chunk_reuse, simulate_async_suite, simulate_frame_skip, simulate_observation_delay, recovery_delay_proxy

def make_actions():
    return np.arange(20, dtype=np.float32).reshape(10, 2)

def test_frame_skip_keeps_shape():
    actions = make_actions()
    result = simulate_frame_skip(actions, skip=2)
    assert result.actions.shape == actions.shape
    assert result.name == "frame_skip"
    assert result.metrics["aligned_steps"] == actions.shape[0]

def test_observation_delay_reuses_old_actions():
    actions = make_actions()
    result = simulate_observation_delay(actions, delay_steps=2)
    assert np.allclose(result.actions[0], actions[0])
    assert np.allclose(result.actions[1], actions[0])
    assert np.allclose(result.actions[2], actions[0])

def test_action_chunk_reuse():
    actions = make_actions()
    result = simulate_action_chunk_reuse(actions, chunk_size=3)
    assert result.actions.shape == actions.shape
    assert np.allclose(result.actions[1], actions[0])
    assert np.allclose(result.actions[2], actions[0])
    assert "chunk_boundary_discontinuity_mean" in result.metrics

def test_async_suite_has_expected_modes():
    results = simulate_async_suite(make_actions())
    names = {r.name for r in results}
    assert "frame_skip" in names
    assert "observation_delay" in names
    assert "action_chunk_reuse" in names
    assert "temporal_jitter" in names
    assert all("recovery_delay_proxy" in r.metrics for r in results)

def test_recovery_delay_proxy_returns_int():
    actions = make_actions()
    result = simulate_frame_skip(actions, skip=2)
    delay = recovery_delay_proxy(actions, result.actions)
    assert isinstance(delay, int)
    assert delay >= 0
