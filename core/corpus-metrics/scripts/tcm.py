#!/usr/bin/env python3
"""Stable front door for other skills: inspect, measure, build norms, or compare a draft.

This launcher is stdlib-only. It discovers a project-local virtual environment before
dispatching to the dependency-bearing scripts, so callers do not need to activate a venv.
Set TCM_PYTHON to an exact interpreter path to override discovery.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent


def python_candidates():
    override = os.environ.get("TCM_PYTHON")
    if override:
        yield Path(override).expanduser()

    seen = set()
    for start in (Path.cwd().resolve(), HERE.parent.resolve()):
        for parent in (start, *start.parents):
            for rel in ((".venv", "Scripts", "python.exe"),
                        (".venv", "bin", "python")):
                candidate = parent.joinpath(*rel)
                key = str(candidate).casefold()
                if key not in seen:
                    seen.add(key)
                    yield candidate

    yield Path(sys.executable)


def find_python():
    for candidate in python_candidates():
        if candidate.is_file():
            return candidate.resolve()
    fallback = shutil.which("python3") or shutil.which("python")
    if fallback:
        return Path(fallback).resolve()
    raise SystemExit("No Python interpreter found. Set TCM_PYTHON to the Tier-1 venv Python.")


def call(python, script, args):
    return subprocess.run([str(python), str(HERE / script), *map(str, args)]).returncode


def measure_args(args, out):
    result = ["--input", args.input, "--tier", args.tier,
              "--spacy-model", args.spacy_model, "--out", out]
    if args.backend:
        result += ["--backend", args.backend]
    if args.tools_dir:
        result += ["--tools-dir", args.tools_dir]
    if getattr(args, "workdir", None):
        result += ["--workdir", args.workdir]
    return result


def add_measurement_options(parser, require_out=False):
    parser.add_argument("--input", required=True,
                        help="draft file or corpus directory containing .txt/.md files")
    parser.add_argument("--tier", type=int, choices=(1, 2), default=1)
    parser.add_argument("--backend", help="comma-separated backend subset")
    parser.add_argument("--tools-dir", help="Tier-2 source tools directory")
    parser.add_argument("--spacy-model", default="en_core_web_md")
    parser.add_argument("--workdir", help="retain backend staging files here")
    if require_out:
        parser.add_argument("--out", required=True, help="tidy metrics CSV")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="check the discovered environment")
    doctor.add_argument("--tools-dir")
    doctor.add_argument("--spacy-model", default="en_core_web_md")
    doctor.add_argument("--json", action="store_true")

    measure = sub.add_parser("measure", help="emit backend metrics as a tidy CSV")
    add_measurement_options(measure, require_out=True)

    build = sub.add_parser("build", help="measure a corpus and build versioned norms")
    add_measurement_options(build)
    build.add_argument("--out", required=True, help="norms JSON")
    build.add_argument("--label", default="")
    build.add_argument("--metrics-out", help="also retain the corpus metrics CSV")

    compare = sub.add_parser("compare", help="measure a draft and compare it with norms")
    add_measurement_options(compare)
    compare.add_argument("--norms", required=True)
    compare.add_argument("--low", type=float, default=10.0)
    compare.add_argument("--top", type=int, default=6)
    compare.add_argument("--all", action="store_true")
    compare.add_argument("--force-provenance", action="store_true")
    compare.add_argument("--csv", help="write the full percentile table")
    compare.add_argument("--metrics-out", help="also retain the draft metrics CSV")

    args = ap.parse_args()
    python = find_python()

    if args.command == "doctor":
        forwarded = ["--spacy-model", args.spacy_model]
        if args.tools_dir:
            forwarded += ["--tools-dir", args.tools_dir]
        if args.json:
            forwarded.append("--json")
        raise SystemExit(call(python, "doctor.py", forwarded))

    if args.command == "measure":
        raise SystemExit(call(python, "run_tools.py", measure_args(args, args.out)))

    with tempfile.TemporaryDirectory(prefix="tcm_facade_") as temp:
        metrics = Path(args.metrics_out).resolve() if args.metrics_out else Path(temp) / "metrics.csv"
        rc = call(python, "run_tools.py", measure_args(args, metrics))
        if rc:
            raise SystemExit(rc)

        if args.command == "build":
            forwarded = ["build", "--metrics", metrics, "--out", args.out,
                         "--source", Path(args.input).resolve()]
            if args.label:
                forwarded += ["--label", args.label]
        else:
            forwarded = ["compare", "--metrics", metrics, "--norms", args.norms,
                         "--low", args.low, "--top", args.top]
            if args.all:
                forwarded.append("--all")
            if args.force_provenance:
                forwarded.append("--force-provenance")
            if args.csv:
                forwarded += ["--csv", args.csv]
        raise SystemExit(call(python, "norms.py", forwarded))


if __name__ == "__main__":
    main()
