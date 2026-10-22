#!/usr/bin/env python3
"""Flag manuscript claims that require manual evidence review.

Built-in patterns are generic. Project-specific patterns are loaded from a ```patterns
fenced block in a rules file (see ``project/claim-risks.md``), one rule per line:

    label :: regex

A flag is a prompt to look, not a verdict, and a clean run is not a passing audit.

Standard library only. Python 3.8+.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

GENERIC_PATTERNS: Dict[str, str] = {
    "causal claim": r"\b(causes?|drives?|mechanism|leads? to|results? in)\b",
    "priority claim": r"\b(first|novel|unprecedented|for the first time)\b",
    "promotional robustness": r"\b(robust|robustly|strongly|powerful|groundbreaking)\b",
    "unsupported proof verb": r"\b(proves?|confirms?|demonstrates?)\b",
    "participant/observation ambiguity": r"\bN\s*=\s*[0-9,]{4,}\b",
    "absence claim": r"\b(no (evidence|effect|difference|association))\b",
    "unhedged generalization": r"\b(all|every|always|never) (participants?|readers?|people)\b",
}

PATTERNS_BLOCK_RE = re.compile(r"```patterns\s*\n(.*?)```", re.DOTALL)
BAD_P_VALUE_RE = re.compile(r"\bp\s*=\s*\.?(000|0000+)\b", re.I)
UNRESOLVED_MARKERS: Sequence[str] = ("TODO", "TBD", "[VERIFY", "[CITATION", "???")

Finding = Tuple[int, str, str]


def load_project_patterns(rules: Optional[Path]) -> Dict[str, str]:
    """Read ``label :: regex`` lines from a ```patterns block in a rules file."""
    patterns: Dict[str, str] = {}
    if rules is None:
        return patterns
    if not rules.is_file():
        print(f"warning: patterns file not found: {rules}", file=sys.stderr)
        return patterns
    block = PATTERNS_BLOCK_RE.search(rules.read_text(encoding="utf-8"))
    if block is None:
        print(f"warning: no ```patterns block in {rules}", file=sys.stderr)
        return patterns
    for line in block.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "::" not in line:
            continue
        label, _, expression = line.partition("::")
        label, expression = label.strip(), expression.strip()
        try:
            re.compile(expression)
        except re.error as exc:
            print(f"warning: invalid regex for {label!r} in {rules}: {exc}", file=sys.stderr)
            continue
        patterns[label] = expression
    return patterns


def scan(lines: Sequence[str], patterns: Dict[str, str]) -> List[Finding]:
    """Return (line number, label, excerpt) for every pattern hit."""
    compiled = [(label, re.compile(expr, re.I)) for label, expr in patterns.items()]
    findings: List[Finding] = []
    for number, line in enumerate(lines, 1):
        excerpt = line.strip()[:240]
        for label, regex in compiled:
            if regex.search(line):
                findings.append((number, label, excerpt))
        if BAD_P_VALUE_RE.search(line):
            findings.append((number, "invalid p-value style", excerpt))
        if any(token in line.upper() for token in UNRESOLVED_MARKERS):
            findings.append((number, "unresolved marker", excerpt))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag manuscript claims that require manual evidence review.",
        epilog="Example: python scripts/audit_draft.py DRAFT.md "
               "--patterns project/claim-risks.md",
    )
    parser.add_argument("manuscript", type=Path, help="Markdown draft to screen")
    parser.add_argument(
        "--patterns",
        type=Path,
        default=None,
        help="rules file with a ```patterns block (e.g. project/claim-risks.md)",
    )
    parser.add_argument(
        "--generic-only",
        action="store_true",
        help="skip project patterns even if a rules file is given",
    )
    args = parser.parse_args()

    if not args.manuscript.is_file():
        print(f"error: no such file: {args.manuscript}", file=sys.stderr)
        return 2

    patterns = dict(GENERIC_PATTERNS)
    if not args.generic_only:
        project_patterns = load_project_patterns(args.patterns)
        patterns.update(project_patterns)
        if args.patterns is not None:
            print(f"Loaded {len(project_patterns)} project pattern(s) from {args.patterns}\n")

    lines = args.manuscript.read_text(encoding="utf-8").splitlines()
    findings = scan(lines, patterns)

    if not findings:
        print(f"{args.manuscript}: no configured claim risks detected; "
              "manual audit is still required")
        return 0

    print(f"{args.manuscript}: {len(findings)} passage(s) require manual review")
    for number, label, excerpt in findings:
        print(f"- line {number} [{label}]: {excerpt}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
