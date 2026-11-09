"""Run the bias probe and write a JSON result file (seed-stamped)."""

import argparse
import json
import pathlib
import platform
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from rlvr_bias_probe import run_experiment  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", type=int, default=200)
    ap.add_argument("--group-size", type=int, default=8)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--verbosity-bonus", type=float, default=0.3)
    ap.add_argument("--out", type=str, default="results/bias-probe.json")
    args = ap.parse_args()

    out = run_experiment(
        groups=args.groups, group_size=args.group_size, seed=args.seed,
        verbosity_bonus=args.verbosity_bonus,
    )
    out["provenance"] = {"python": platform.python_version(), "platform": platform.platform()}
    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out["arms"], indent=2))


if __name__ == "__main__":
    main()
