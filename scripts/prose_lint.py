#!/usr/bin/env python3
"""Flag common clarity and calibration risks without rewriting text.

Built-in replacements are generic. Project-specific ones can be added in a ```terms fenced
block in any rules file (see ``project/lexicon.md``), one rule per line:

    phrase to avoid :: what to do instead

Every flag is a prompt for judgment. Do not mechanically accept them.

Standard library only. Python 3.8+.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

TERMS: Dict[str, str] = {
    "utilize": "use",
    "in order to": "to",
    "due to the fact that": "because",
    "it is important to note": "state the point directly",
    "it is worth noting": "state the point directly",
    "the present study": "this study / we",
    "plays a crucial role": "specify the relation",
    "has the ability to": "can",
    "conducted an examination of": "examined",
    "groundbreaking": "state the concrete contribution",
    "robustly": "name the robustness evidence or remove",
    "proves": "use a calibrated evidence verb",
    "confirms": "consider supports / is consistent with",
}

TERMS_BLOCK_RE = re.compile(r"```terms\s*\n(.*?)```", re.DOTALL)
CAUSAL_RE = re.compile(
    r"\b(causes?|caused|drives?|driven|mechanism|explains?|leads? to|results? in)\b", re.I
)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
VAGUE_PRONOUN_RE = re.compile(
    r"\b(this|it|they)\s+(shows|suggests|demonstrates|indicates)\b", re.I
)

LONG_SENTENCE_WORDS = 40


def load_project_terms(rules: Optional[Path]) -> Dict[str, str]:
    """Read ``phrase :: suggestion`` lines from a ```terms block in a rules file."""
    terms: Dict[str, str] = {}
    if rules is None:
        return terms
    if not rules.is_file():
        print(f"warning: terms file not found: {rules}", file=sys.stderr)
        return terms
    block = TERMS_BLOCK_RE.search(rules.read_text(encoding="utf-8"))
    if block is None:
        return terms
    for line in block.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "::" not in line:
            continue
        phrase, _, suggestion = line.partition("::")
        terms[phrase.strip().lower()] = suggestion.strip()
    return terms


def scan(text: str, terms: Dict[str, str]) -> List[str]:
    """Return one message per possible issue found."""
    issues: List[str] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        lower = line.lower()
        for term, suggestion in terms.items():
            if term in lower:
                issues.append(f"line {lineno}: '{term}' -> {suggestion}")
        causal = {match.group(0) for match in CAUSAL_RE.finditer(line)}
        if causal:
            found = ", ".join(sorted(causal, key=str.lower))
            issues.append(
                f"line {lineno}: causal/mechanistic language requires design support: {found}"
            )
        for sentence in SENTENCE_RE.split(line):
            count = len(WORD_RE.findall(sentence))
            if count > LONG_SENTENCE_WORDS:
                issues.append(
                    f"line {lineno}: {count}-word sentence; inspect structure "
                    "(not an automatic error)"
                )
        if VAGUE_PRONOUN_RE.search(line):
            issues.append(f"line {lineno}: check pronoun referent in evidence claim")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag common clarity and calibration risks without rewriting text.",
        epilog="Example: python scripts/prose_lint.py DRAFT.md --terms project/lexicon.md",
    )
    parser.add_argument("manuscript", type=Path, help="Markdown or text draft to screen")
    parser.add_argument(
        "--terms",
        type=Path,
        default=None,
        help="rules file with a ```terms block (e.g. project/lexicon.md)",
    )
    args = parser.parse_args()

    if not args.manuscript.is_file():
        print(f"error: no such file: {args.manuscript}", file=sys.stderr)
        return 2

    terms = dict(TERMS)
    terms.update(load_project_terms(args.terms))

    issues = scan(args.manuscript.read_text(encoding="utf-8"), terms)
    if issues:
        print(f"{args.manuscript}: {len(issues)} possible issue(s)")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"{args.manuscript}: no configured prose risks detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
