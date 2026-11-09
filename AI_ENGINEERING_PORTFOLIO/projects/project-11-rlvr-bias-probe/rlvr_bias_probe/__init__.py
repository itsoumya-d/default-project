"""rlvr-bias-probe: estimator comparison for verifiable-reward RL.

Simulated-policy experiment: a synthetic environment where completion length
yearns a spurious reward (verbosity bonus) that is *not* the solve signal.
Compare the standard GRPO advantage (mean/std normalization, broadcast to
tokens) against Dr. GRPO (mean-center only, constant token normalization)
and measure length drift vs solve rate.

Everything is deterministic given a seed. No LLM, no GPU.
"""

from __future__ import annotations

import json
import math
import statistics
from dataclasses import dataclass, field


@dataclass
class SimEnv:
    """One prompt = one Bernoulli solve chance + a verbosity bonus.

    A completion is (solved: bool, length: int). reward = 1.0*solved
    + verbosity_bonus * normalized_length, where normalized_length is
    length / max_len in [0, 1]. The verbosity bonus is spurious: a good
    policy must increase solve rate, not length.
    """

    verbosity_bonus: float = 0.3
    max_len: int = 200
    base_solve: float = 0.25

    def sample(self, rng, skill: float, verbosity: float) -> dict:
        """skill: 0..1 (ability to solve); verbosity: 0..1 (length propensity)."""
        solve_p = max(0.0, min(1.0, self.base_solve + skill))
        solved = rng.random() < solve_p
        length = int(
            (0.1 + 0.9 * verbosity) * self.max_len * rng.uniform(0.5, 1.0)
        )
        reward = (1.0 if solved else 0.0) + self.verbosity_bonus * (length / self.max_len)
        return {"solved": solved, "length": length, "reward": reward}


def grpo_advantages(rewards: list[float]) -> list[float]:
    """Standard GRPO: (r - mean) / std, broadcast per completion."""
    mu = statistics.fmean(rewards)
    sd = statistics.pstdev(rewards) or 1.0
    return [(r - mu) / sd for r in rewards]


def drgrpo_advantages(rewards: list[float]) -> list[float]:
    """Dr. GRPO: mean-centered only, no std division (bias removal)."""
    mu = statistics.fmean(rewards)
    return [r - mu for r in rewards]


@dataclass
class EstimatorResult:
    name: str
    mean_length: float
    solve_rate: float
    length_drift: float
    adv_length_corr: float
    mean_reward: float
    groups: int = field(default=0)


def _pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def run_experiment(*, groups: int = 200, group_size: int = 8, seed: int = 42,
                   verbosity_bonus: float = 0.3, lr: float = 0.02,
                   steps: int = 30) -> dict:
    """Bandit-style policy update loop over a scalar skill/verbosity policy.

    Two arms (GRPO, Dr.GRPO) start from the same init and share the same
    sampled completions per round; each arm updates its own (skill, verbosity)
    with its estimator's advantages. We track length drift vs solve rate.
    """
    import random

    env = SimEnv(verbosity_bonus=verbosity_bonus)
    arms = {
        name: {"skill": 0.0, "verbosity": 0.5, "adv_fn": fn}
        for name, fn in (("grpo", grpo_advantages), ("drgrpo", drgrpo_advantages))
    }
    init_len = {name: [] for name in arms}
    adv_len_pairs = {name: ([], []) for name in arms}
    lengths = {name: [] for name in arms}
    solves = {name: [] for name in arms}
    rewards = {name: [] for name in arms}

    for g in range(groups):
        rng = random.Random(seed * 10_000 + g)
        # Sample one shared batch per group from the *average* policy state.
        avg_skill = statistics.fmean(a["skill"] for a in arms.values())
        avg_verb = statistics.fmean(a["verbosity"] for a in arms.values())
        batch = [env.sample(rng, avg_skill, avg_verb) for _ in range(group_size)]
        rs = [c["reward"] for c in batch]
        for name, a in arms.items():
            advs = a["adv_fn"](rs)
            # Policy gradient on (skill, verbosity): d(reward)/d(policy-item).
            # solved completions push skill up; reward correlates with length,
            # so both are pushed toward whatever the estimator rewards.
            g_skill = statistics.fmean(
                adv * (1.0 if c["solved"] else 0.0) for adv, c in zip(advs, batch)
            )
            g_verb = statistics.fmean(
                adv * ((c["length"] / env.max_len) - 0.5) for adv, c in zip(advs, batch)
            )
            a["skill"] = max(0.0, min(1.0, a["skill"] + lr * g_skill))
            a["verbosity"] = max(0.0, min(1.0, a["verbosity"] + lr * g_verb))
            for adv, c in zip(advs, batch):
                adv_len_pairs[name][0].append(adv)
                adv_len_pairs[name][1].append(c["length"] / env.max_len)
            if g == 0:
                init_len[name] = [c["length"] for c in batch]
            lengths[name].extend(c["length"] for c in batch)
            solves[name].extend(1.0 if c["solved"] else 0.0 for c in batch)
            rewards[name].extend(rs)

    out = {"env": {"verbosity_bonus": verbosity_bonus, "max_len": env.max_len},
           "groups": groups, "group_size": group_size, "seed": seed, "arms": {}}
    for name in arms:
        advs, lns = adv_len_pairs[name]
        mean_len = statistics.fmean(lengths[name])
        out["arms"][name] = {
            "mean_length": mean_len,
            "solve_rate": statistics.fmean(solves[name]),
            "mean_reward": statistics.fmean(rewards[name]),
            "length_drift": mean_len - statistics.fmean(init_len[name]),
            "adv_length_corr": _pearson(advs, lns),
            "final_skill": arms[name]["skill"],
            "final_verbosity": arms[name]["verbosity"],
        }
    return out
