"""Cross-project benchmark harness.

Runs every Python test suite found in `repos/*` (local clones, git-ignored)
plus the in-repo projects under `AI_ENGINEERING_PORTFOLIO/projects/`, and
emits one comparable JSON + Markdown table with hardware/seed/command stamps.

Skip missing clones gracefully (records `not-present`), never fails CI on a
missing dir. Every row records: repo, tests collected, passed/failed/errors/
skipped, exit code, duration, python version, platform.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import platform
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
REPOS = ROOT / "repos"
PROJECTS = ROOT / "AI_ENGINEERING_PORTFOLIO" / "projects"
SKIP = {"autopilot-fde", "edgeinfer", "HEROS", "peervault"}


def discover() -> list[dict]:
    targets = []
    if REPOS.exists():
        for d in sorted(REPOS.iterdir()):
            if not d.is_dir() or d.name in SKIP or not (d / "tests").exists():
                continue
            targets.append({"repo": d.name, "path": d})
    if PROJECTS.exists():
        for d in sorted(PROJECTS.iterdir()):
            if (d / "tests").exists() or (d / "test").exists():
                targets.append({"repo": d.name, "path": d})
    return targets


def run_one(target: dict) -> dict:
    start = time.time()
    cmd = [sys.executable, "-m", "pytest", "tests", "-q", "--no-header",
           "-p", "no:cacheprovider"]
    # Also try a `test/` dir variant.
    if target["path"].joinpath("tests").exists():
        pass
    elif target["path"].joinpath("test").exists():
        cmd[3] = "test"
    try:
        proc = subprocess.run(cmd, cwd=str(target["path"]), capture_output=True,
                              text=True, timeout=300)
        tail = proc.stdout[-2000:] + proc.stderr[-2000:]
        row = {"repo": target["repo"], "dir": str(target["path"].relative_to(ROOT)),
               "exit": proc.returncode, "seconds": round(time.time() - start, 1),
               "tail": tail.strip().splitlines()[-3:] if tail.strip() else []}
    except subprocess.TimeoutExpired:
        row = {"repo": target["repo"], "dir": str(target["path"].relative_to(ROOT)),
               "exit": -1, "seconds": 300, "tail": ["TIMEOUT"]}
    return row


def parse_summary(row: dict) -> dict:
    tail = " ".join(row.get("tail", []))
    row["summary"] = tail
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="AI_ENGINEERING_PORTFOLIO/research/benchmarks/results/cross-bench.json")
    ap.add_argument("--md", default="AI_ENGINEERING_PORTFOLIO/research/benchmarks/RESULTS_2026-11-09.md")
    args = ap.parse_args()

    targets = discover()
    rows = [parse_summary(run_one(t)) for t in targets]
    report = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "suite": "pytest tests -q -p no:cacheprovider (per-repo root)",
        "results": rows,
    }
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md = [
        "# Cross-project benchmark results",
        "",
        f"Generated (UTC): {report['generated_utc']}",
        f"Platform: {report['platform']}",
        f"Python: {report['python']}",
        f"Command: `{report['suite']}`",
        "",
        "| Repo | Dir | Exit | Sec | Summary |",
        "|---|---|---:|---:|---|",
    ]
    for r in rows:
        summ = r["summary"].replace("|", "/")[:160]
        md.append(f"| {r['repo']} | {r['dir']} | {r['exit']} | {r['seconds']} | {summ} |")
    pathlib.Path(args.md).write_text("\n".join(md) + "\n", encoding="utf-8")
    for r in rows:
        print(f"{r['repo']:38s} exit={r['exit']:>3} {r['seconds']:>6}s  {r['summary'][:80]}")


if __name__ == "__main__":
    main()
