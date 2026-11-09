"""Stage (and optionally publish) HF artifacts for the portfolio.

Default is a dry run: writes a manifest of what would be uploaded and does NOT
require a token. To publish:

    python publish_hf.py --publish --token hf_xxx

or set HF_TOKEN, or `huggingface-cli login` first.

What it stages:
  1. Model: itssoumyad/heros-rlvr-qwen2.5-coder-1.5b  (P01 checkpoint-100 LoRA
     + adapter_config/editor tokenizer + MODEL_CARD.md)
  2. Dataset: itssoumyad/rlvr-bias-probe-results     (results/bias-probe.json
     + estimator/seed report from project-11)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve()
PORTFOLIO = HERE.parent.parent  # AI_ENGINEERING_PORTFOLIO/
MODEL_SRC = (
    PORTFOLIO / "projects/project-01-heros-rlvr-studio/runs"
    "/2026-11-03-rl-base-100-corrected/checkpoint-100"
)
BIAS_RESULTS = (
    PORTFOLIO / "projects/project-11-rlvr-bias-probe/results/bias-probe.json"
)
CARD = HERE.parent / "MODEL_CARD.md"
MODEL_ID = "itssoumyad/heros-rlvr-qwen2.5-coder-1.5b"
DATASET_ID = "itssoumyad/rlvr-bias-probe-results"


def sha(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:12]


def manifest() -> dict:
    files = []
    for f in sorted(MODEL_SRC.iterdir()):
        files.append({"name": f.name, "bytes": f.stat().st_size, "sha12": sha(f)})
    out = {"model": MODEL_ID, "source_dir": str(MODEL_SRC), "files": files}
    if BIAS_RESULTS.exists():
        out["dataset"] = {"id": DATASET_ID, "source": str(BIAS_RESULTS),
                          "sha12": sha(BIAS_RESULTS)}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--token", type=str, default=None)
    args = ap.parse_args()

    man = manifest()
    print(json.dumps(man, indent=2))
    if not args.publish:
        print("\n(dry run — pass --publish --token to upload to HF)")
        return

    from huggingface_hub import HfApi

    import os
    token = args.token or os.environ.get("HF_TOKEN")
    if not token:
        sys.exit("No HF token: pass --token or set HF_TOKEN (huggingface-cli login).")
    api = HfApi(token=token)

    api.create_repo(repo_id=MODEL_ID, repo_type="model", exist_ok=True)
    for f in sorted(MODEL_SRC.iterdir()):
        api.upload_file(
            path_or_fileobj=str(f), path_in_repo=f.name,
            repo_id=MODEL_ID, repo_type="model", commit_message=f"add {f.name}")
    api.upload_file(
        path_or_fileobj=str(CARD), path_in_repo="README.md",
        repo_id=MODEL_ID, repo_type="model",
        commit_message="add model card (adapter trained for 91 steps; no benchmark gain claimed)")

    api.create_repo(repo_id=DATASET_ID, repo_type="dataset", exist_ok=True)
    api.upload_file(
        path_or_fileobj=str(BIAS_RESULTS), path_in_repo="bias-probe.json",
        repo_id=DATASET_ID, repo_type="dataset",
        commit_message="add rlvr-bias-probe results (seed-stamped)")
    api.upload_file(
        path_or_fileobj=str(PORTFOLIO / "projects/project-11-rlvr-bias-probe/README.md"),
        path_in_repo="README.md", repo_id=DATASET_ID, repo_type="dataset",
        commit_message="add probe README + methods")
    print("published:", MODEL_ID, "and", DATASET_ID)


if __name__ == "__main__":
    main()
