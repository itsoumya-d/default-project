"""Test rlvr-bias-probe estimator functions + full experiment."""

import statistics

from rlvr_bias_probe import (
    drgrpo_advantages,
    grpo_advantages,
    run_experiment,
)


def test_grpo_zero_mean_zero_var():
    adv = grpo_advantages([0.5, 0.5, 0.5])
    assert all(abs(a) < 1e-9 for a in adv)


def test_grpo_basic():
    adv = grpo_advantages([0.0, 1.0])
    assert adv[0] < 0 < adv[1]
    assert abs(statistics.fmean(adv)) < 1e-9


def test_drgrpo_mean_centered_only():
    # Identical rewards -> zero advantage, and mean of advantages is zero.
    adv = drgrpo_advantages([0.2, 0.2, 0.2])
    assert all(abs(a) < 1e-9 for a in adv)
    adv2 = drgrpo_advantages([0.0, 1.0, 2.0])
    assert abs(statistics.fmean(adv2)) < 1e-9
    # Dr.GRPO scale differs from GRPO (no std division).
    g = grpo_advantages([0.0, 1.0, 2.0])
    d = drgrpo_advantages([0.0, 1.0, 2.0])
    assert abs(g[2]) != abs(d[2])


def test_experiment_is_deterministic():
    a = run_experiment(groups=20, group_size=4, seed=7)
    b = run_experiment(groups=20, group_size=4, seed=7)
    assert a == b


def test_experiment_verbosity_bonus_changes_behavior():
    hi = run_experiment(groups=60, group_size=8, seed=42, verbosity_bonus=0.9)
    lo = run_experiment(groups=60, group_size=8, seed=42, verbosity_bonus=0.0)
    # With a strong spurious verbosity bonus, lengths drift up more.
    assert hi["arms"]["grpo"]["length_drift"] > lo["arms"]["grpo"]["length_drift"]


def test_experiment_output_schema():
    out = run_experiment(groups=10, group_size=4, seed=1)
    assert set(out["arms"]) == {"grpo", "drgrpo"}
    for arm in out["arms"].values():
        for k in ("mean_length", "solve_rate", "mean_reward",
                  "length_drift", "adv_length_corr",
                  "final_skill", "final_verbosity"):
            assert k in arm
        assert 0.0 <= arm["solve_rate"] <= 1.0
        assert -1.0 <= arm["adv_length_corr"] <= 1.0
