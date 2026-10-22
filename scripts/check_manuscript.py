#!/usr/bin/env python3
"""Screen a Markdown manuscript against a venue profile.

A deterministic preflight, not an editorial or statistical review. Venue limits are read from
a profile file (see ``project/venue-target.md``) so this script stays venue- and
field-agnostic.

Standard library only. Python 3.8+.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
HEADING_RE = re.compile(
    r"^(?:#{1,6}\s*)?"
    r"(Abstract|Introduction|Intro|Methods?|Results?|Discussion|General Discussion|"
    r"Research Transparency Statement|Transparency Statement|Outline|OLD VERSION):?\s*$",
    re.MULTILINE | re.IGNORECASE,
)
LIMITS_BLOCK_RE = re.compile(r"```limits\s*\n(.*?)```", re.DOTALL)
CAUSAL_RE = re.compile(r"\b(causes?|caused|drives?|driven|mechanism|explains?)\b", re.I)
BAD_P_VALUE_RE = re.compile(r"\bp\s*[=<>]\s*0?\.000\b", re.I)

DEFAULT_LIMITS: Dict[str, int] = {
    "abstract_max_words": 150,
    "front_back_max_words": 2000,
    "method_results_target_words": -1,
    "reference_target_count": -1,
}

UNRESOLVED_MARKERS: Sequence[str] = ("TODO", "TBD", "[CITATION", "[VERIFY", "???")


def words(text: str) -> int:
    """Prose word count via the shared function, so it matches the ingestion screen's."""
    try:
        from textmetrics import prose_words
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from textmetrics import prose_words
    return prose_words(text)


def sections(text: str) -> Dict[str, str]:
    """Split a draft into a {lowercased heading: body} map.

    Delegates to the shared parser. The local HEADING_RE recognised `## Abstract` but not
    `**Abstract**`, so bold-headed drafts reported "Abstract: 0 / 150" -- a silent pass on the check
    that most often causes desk rejection.
    """
    try:
        from textmetrics import parse_sections
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from textmetrics import parse_sections
    return parse_sections(text)


def find_section(parts: Dict[str, str], names: Iterable[str]) -> str:
    """Return the first section body whose heading contains any of ``names``."""
    for heading, body in parts.items():
        if any(name in heading for name in names):
            return body
    return ""


def load_limits(profile: Optional[Path]) -> Dict[str, int]:
    """Read a ```limits fenced block from a venue profile; missing keys fall back."""
    limits = dict(DEFAULT_LIMITS)
    if profile is None:
        return limits
    if not profile.is_file():
        print(f"warning: profile not found: {profile}; using built-in defaults", file=sys.stderr)
        return limits
    block = LIMITS_BLOCK_RE.search(profile.read_text(encoding="utf-8"))
    if block is None:
        print(f"warning: no ```limits block in {profile}; using built-in defaults", file=sys.stderr)
        return limits
    for line in block.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        try:
            limits[key.strip()] = int(raw.strip())
        except ValueError:
            print(f"warning: non-integer limit {key.strip()!r} in {profile}", file=sys.stderr)
    return limits


def collect_warnings(text: str, parts: Dict[str, str], limits: Dict[str, int]) -> List[str]:
    """Return every screening warning for this draft."""
    abstract = find_section(parts, ("abstract",))
    intro = find_section(parts, ("introduction", "intro"))
    discussion = find_section(parts, ("discussion",))
    transparency = find_section(parts, ("research transparency", "transparency statement"))
    method = find_section(parts, ("method",))
    results = find_section(parts, ("results",))

    abstract_max = limits["abstract_max_words"]
    front_back_max = limits["front_back_max_words"]

    warnings: List[str] = []
    if abstract and abstract_max >= 0 and words(abstract) > abstract_max:
        warnings.append(f"Abstract exceeds {abstract_max} words.")
    if intro and discussion and front_back_max >= 0:
        if words(intro) + words(discussion) > front_back_max:
            warnings.append(
                f"Introduction + Discussion already exceed {front_back_max} words "
                "before other counted material."
            )
    if not transparency:
        warnings.append("Transparency statement not detected.")
    if not method or not results:
        warnings.append("Separate Method and Results headings were not both detected.")
    for marker in UNRESOLVED_MARKERS:
        if marker.lower() in text.lower():
            warnings.append(f"Unresolved marker detected: {marker}")
    causal = CAUSAL_RE.findall(text)
    if causal:
        warnings.append(
            "Causal/mechanistic terms require design-level justification: "
            + ", ".join(sorted({term.lower() for term in causal}))
        )
    if BAD_P_VALUE_RE.search(text):
        warnings.append("Report very small p values as p < .001, never p = .000.")
    return warnings


def report(manuscript: Path, profile: Optional[Path], parts: Dict[str, str],
           text: str, limits: Dict[str, int]) -> None:
    """Print the descriptive half of the screen."""
    abstract_max = limits["abstract_max_words"]
    front_back_max = limits["front_back_max_words"]
    intro_words = words(find_section(parts, ("introduction", "intro")))
    discussion_words = words(find_section(parts, ("discussion",)))

    print(f"Manuscript: {manuscript}")
    if profile is not None:
        print(f"Profile:    {profile}")
    print(f"Total words (rough Markdown count): {words(text)}")
    abstract_budget = f" / {abstract_max}" if abstract_max >= 0 else " (no limit set)"
    print(f"Abstract: {words(find_section(parts, ('abstract',)))}{abstract_budget}")
    print(f"Introduction: {intro_words}")
    print(f"Discussion: {discussion_words}")
    front_back_budget = (
        f" / {front_back_max} (counted extras not included)"
        if front_back_max >= 0 else " (no limit set)"
    )
    print(f"Introduction + Discussion: {intro_words + discussion_words}{front_back_budget}")
    print(f"Method present: {'yes' if find_section(parts, ('method',)) else 'NO'}")
    print(f"Results present: {'yes' if find_section(parts, ('results',)) else 'NO'}")
    transparency = find_section(parts, ("research transparency", "transparency statement"))
    print(f"Transparency statement present: {'yes' if transparency else 'NO'}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Screen a Markdown manuscript against a venue profile.",
        epilog="Example: python scripts/check_manuscript.py DRAFT.md "
               "--profile project/venue-target.md",
    )
    parser.add_argument("manuscript", type=Path, help="Markdown draft to screen")
    parser.add_argument(
        "--profile",
        type=Path,
        default=None,
        help="venue profile containing a ```limits block (e.g. project/venue-target.md)",
    )
    args = parser.parse_args()

    if not args.manuscript.is_file():
        print(f"error: no such file: {args.manuscript}", file=sys.stderr)
        return 2

    limits = load_limits(args.profile)
    text = args.manuscript.read_text(encoding="utf-8")
    parts = sections(text)

    report(args.manuscript, args.profile, parts, text, limits)
    warnings = collect_warnings(text, parts, limits)

    print("\nWarnings:")
    if warnings:
        for item in warnings:
            print(f"- {item}")
        return 1
    print("- None detected by this limited screen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
