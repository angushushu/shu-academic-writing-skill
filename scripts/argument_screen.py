#!/usr/bin/env python3
"""Screen a manuscript's argument surfaces: is the answer where a reader looks for it?

Three screens, each anchored on a defect that was measured on a constructed argument-damage
case (the paper's argument was damaged sentence-by-sentence, prose left verbatim; the clean
reference passes every screen, the damaged draft fails two of them):

  A. the abstract states a finding and carries no gap framing -- checked over the whole
     abstract, not only its opening (a gap sentence after a stake still spends abstract space on
     what nobody has done instead of what is now known; it belongs in Related Work)
  B. the introduction's CLOSING SENTENCE states the paper's answer, not only a results preview
     (paragraph-level answer language is not enough: the last sentence a reader takes from the
     introduction must be the finding; measured against v2 A2 on 29 frozen manuscripts, 29/29)
  C. limitations inside the Results: a sentence that states a limitation belongs in Limitations.
     Claim calibrations ("we do not claim ...", "should be read with") are listed as notes, not
     flags -- a paper may legitimately calibrate a claim where the claim is made.

A flag is a prompt to read the printed sentence, not a verdict, and a clean run is not a
passing argument review. Standard library only. Python 3.8+.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

# Screen vocabularies. They are deliberately small and anchored on the measured case: detectors
# for a defect class, not a style score. Both the failure to state an answer and a false alarm
# are cheap to check by reading the sentence the screen prints.
GAP_PATTERNS: Tuple[Tuple[str, str], ...] = (
    ("has not formalised", r"has not (?:been )?formalis(?:ed|ing)"),
    ("has not formalized", r"has not (?:been )?formaliz(?:ed|ing)"),
    ("no study has", r"no study (?:has|we|to date)"),
    ("little is known", r"little is known"),
    ("remains understudied", r"remains (?:understudied|unclear|poorly)"),
    ("largely unexamined", r"largely unexamined"),
    ("not been systematically", r"not been systematically"),
    ("the literature has not", r"the literature has not"),
)
# Answer language: phrases that state what the paper establishes. Kept strict on purpose -- a
# generic phrase like "the result" is not answer language, it is Results-section vocabulary.
ANSWER_MARKERS: Tuple[str, ...] = (
    "we find", "we show", "we report", "we establish", "we argue", "we ask", "we test",
    "we conclude", "this paper", "the answer", "is not what it appears", "contribution",
)
ABSTRACT_FINDING_MARKERS: Tuple[str, ...] = ANSWER_MARKERS + (
    "does not measure", "fails where", "reproduces", "the pattern",
)
# Screen C separates two kinds of "caveat" sentence. A limitation statement belongs in the
# Limitations section even when the claim it qualifies is interesting; a claim calibration states
# how strongly the claim made where it stands should be read and may stay. The clean reference for
# this screen keeps one calibration sentence in Results ("...so we do not claim that steering
# provably carries no causal information") and no limitation statements there.
LIMITATION_MARKERS: Tuple[str, ...] = (
    "a limitation", "one limitation", "we do not identify", "cannot identify", "cannot generalise",
    "cannot generalize", "may not generalise", "may not generalize", "a caveat",
    "we have not surveyed", "we cannot",
)
CALIBRATION_MARKERS: Tuple[str, ...] = (
    "we do not claim", "we make the weaker point", "should be read with", "it is worth noting",
)
LIMIT_MARKERS: Tuple[str, ...] = LIMITATION_MARKERS + CALIBRATION_MARKERS
# A limitation word inside a denied or rhetorical construction names the concept in order to deny
# it ("each is a test we can run rather than a caveat we can add"); it is not a caveat.
NEGATED_MENTION = re.compile(
    r"(?:rather\s+than|instead\s+of|without|never|no\s+need\s+for|not(?:\s+merely)?|"
    r"(?:is|are|was|were|do|does|did)n't)\s*$",
    re.IGNORECASE,
)
NEGATION_LOOKBACK = 48
NUMBERED_TOP = re.compile(r"^\d+\.?\s")

ATX_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
BOLD_HEADING = re.compile(r"^\*\*(.{1,80}?)\*\*\s*:?\s*$")


Section = Tuple[int, str, str]  # (level, heading, body)


def split_sections(text: str) -> List[Section]:
    """Split a Markdown draft into (level, heading, body) triples.

    ATX headings carry their '#' count as level; a whole-line bold pseudo-heading is treated as
    level 2, so a document without ATX headings still splits. The reader receives text, not a
    file, so a leading BOM is not part of the first heading.
    """
    text = text.lstrip("\ufeff")
    out: List[Section] = []
    level, head, buf = 0, "", []
    for line in text.splitlines():
        atx = ATX_HEADING.match(line)
        bold = BOLD_HEADING.match(line)
        if atx or bold:
            if head or any(part.strip() for part in buf):
                out.append((level, head, "\n".join(buf)))
            if atx:
                level, head = len(atx.group(1)), atx.group(2).strip()
            else:
                level, head = 2, bold.group(1).strip()
            buf = []
        else:
            buf.append(line)
    if head or any(part.strip() for part in buf):
        out.append((level, head, "\n".join(buf)))
    return out


def with_descendants(sections: Sequence[Section], index: int) -> str:
    """Body of a section plus every subsection body beneath it."""
    level = sections[index][0]
    parts = [sections[index][2]]
    for body_level, _head, body in sections[index + 1:]:
        if body_level <= level:
            break
        parts.append(body)
    return "\n".join(parts)


def sentences(text: str) -> List[str]:
    text = re.sub(r"(?m)^#.*$", "", text)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if len(s.split()) >= 4]


def paragraphs(text: str) -> List[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def find_sections(sections: Sequence[Section], *keys: str) -> List[int]:
    return [i for i, (_level, head, _body) in enumerate(sections)
            if head and any(key in head.lower() for key in keys)]


def looks_like_results(heading: str) -> bool:
    low = heading.lower()
    if "result" in low or "finding" in low:
        return True
    return bool(NUMBERED_TOP.match(heading)) and any(
        key in low for key in ("study", "experiment", "audit", "analysis"))


def gap_markers(text: str) -> List[str]:
    low = text.lower()
    return [label for label, pattern in GAP_PATTERNS if re.search(pattern, low)]


def classify_caveats(sentence: str) -> Tuple[List[str], List[str]]:
    """Return (limitation markers, calibration markers) asserted in `sentence`.

    A marker occurrence is ignored when a negation/rhetorical cue immediately precedes it: the
    sentence names the concept in order to deny it, not to qualify a claim.
    """
    low = sentence.lower()
    limitations: List[str] = []
    calibrations: List[str] = []
    for marker in LIMIT_MARKERS:
        start = 0
        while True:
            index = low.find(marker, start)
            if index < 0:
                break
            start = index + 1
            if NEGATED_MENTION.search(low[max(0, index - NEGATION_LOOKBACK):index]):
                continue
            if marker in LIMITATION_MARKERS:
                limitations.append(marker)
            else:
                calibrations.append(marker)
    return limitations, calibrations


def screen_abstract(sections: Sequence[Section]) -> Optional[Dict[str, object]]:
    """Screen A: the abstract states a finding and carries no gap framing anywhere.

    The rule is whole-abstract on purpose. The version of this screen that only checked the
    opening two sentences passed two package runs whose abstracts still contained
    "No study we build on has formalised the check" after the opening -- the same defect the
    v2 A1 property scored 0.00 for. Measured on 25 frozen empirical-case manuscripts, the
    whole-abstract rule agrees with the v2 A1 property 25/25 (the opening-only rule: 20/25).
    """
    indices = find_sections(sections, "abstract")
    if not indices:
        return None
    body = sections[indices[0]][2]
    low = body.lower()
    gaps = gap_markers(body)
    findings = [m for m in ABSTRACT_FINDING_MARKERS if m in low]
    reasons: List[str] = []
    if gaps:
        reasons.append("the abstract contains gap framing (move it to Related Work or the "
                       "introduction's first paragraph)")
    if not findings:
        reasons.append("the abstract does not state a finding")
    return {"name": "abstract states a finding and carries no gap framing", "flagged": bool(reasons),
            "caveats": [], "gaps": gaps, "findings": findings,
            "reason": "; ".join(reasons), "excerpt": (paragraphs(body) or [""])[0]}


def screen_introduction_close(sections: Sequence[Section]) -> Optional[Dict[str, object]]:
    """Screen B: the introduction's CLOSING SENTENCE carries the answer.

    The paragraph-level rule this screen shipped with passed an artifact whose closing paragraph
    stated the finding and then ended on a result detail -- the last sentence a reader takes away was
    evidence, not the finding (measured on the post-A1-edit batch, gen73/gens 76). The rule is now
    the closing sentence. Validated before the edit's measurement: on 29 frozen empirical-case
    manuscripts this rule agrees with property-span v2 A2 = 1.0 on 29/29 (the paragraph rule: 21/29);
    the clean reference passes and the damaged draft fails.
    """
    indices = find_sections(sections, "introduction")
    if not indices:
        return None
    tail = paragraphs(sections[indices[0]][2])
    last = tail[-1] if tail else ""
    closing = sentences(last)
    last_sentence = closing[-1] if closing else last
    low = last_sentence.lower()
    answers = [m for m in ANSWER_MARKERS if m in low]
    return {"name": "introduction closes on the answer",
            "flagged": bool(last_sentence) and not answers,
            "caveats": [], "gaps": [], "findings": answers, "reason": "",
            "excerpt": last_sentence}


def screen_results_caveats(sections: Sequence[Section]) -> Optional[Dict[str, object]]:
    indices = [i for i, (_level, head, _body) in enumerate(sections)
               if head and looks_like_results(head)]
    if not indices:
        return None
    limitations: List[str] = []
    calibrations: List[str] = []
    for index in indices:
        for sentence in sentences(with_descendants(sections, index)):
            limitations_found, calibrations_found = classify_caveats(sentence)
            if limitations_found:
                limitations.append(sentence)
            elif calibrations_found:
                calibrations.append(sentence)
    return {"name": "no limitations inside Results", "flagged": bool(limitations),
            "caveats": limitations, "calibrations": calibrations, "gaps": [], "findings": [],
            "reason": ("a limitation stated where the claim is made belongs in Limitations"
                       if limitations else ""),
            "excerpt": ""}


def run(path: Path) -> int:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    sections = split_sections(text)
    screens = [
        screen_abstract(sections),
        screen_introduction_close(sections),
        screen_results_caveats(sections),
    ]
    ran = [s for s in screens if s is not None]
    if not ran:
        print(f"{path}: no Abstract, Introduction, or Results-like section found; "
              "this screen did not run")
        return 0

    print(f"{path}")
    print(f"  sections found: {len(sections)}")
    flagged = 0
    for screen in ran:
        mark = "FLAG" if screen["flagged"] else "ok  "
        if screen["flagged"]:
            flagged += 1
        print(f"  [{mark}] {screen['name']}")
        if screen["reason"]:
            print(f"         {screen['reason']}")
        if screen["gaps"]:
            print(f"         gap language: {', '.join(str(x) for x in screen['gaps'])}")
        if screen["findings"]:
            label = "caveats" if str(screen["name"]).startswith("qualifications") else "answer language"
            print(f"         {label}: {', '.join(str(x) for x in screen['findings'])}")
        if screen["caveats"]:
            quantity = "one sentence" if len(screen["caveats"]) == 1 else f"{len(screen['caveats'])} sentences"
            print(f"         {quantity} to read -- move each to Limitations unless the paper's "
                  "argument needs it here:")
            for sentence in screen["caveats"]:
                print(f"           - {re.sub(r'[ \t\r\n]+', ' ', sentence)[:300]}")
        calibrations = screen.get("calibrations") or []
        if calibrations:
            print(f"         note (may stay): {len(calibrations)} claim calibration sentence(s) "
                  "in Results")
        if screen["excerpt"]:
            excerpt = re.sub(r"\s+", " ", str(screen["excerpt"]))
            print(f"         read this: {excerpt[:600]}")
    missing = [name for name, screen in zip(
        ("abstract", "introduction", "results"), screens) if screen is None]
    if missing:
        print(f"  note: no {', '.join(missing)} section found; that screen did not run")
    print()
    print("  A flag is a prompt to read the printed sentence, not a verdict.")
    return 1 if flagged else 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Screen a manuscript's argument surfaces: answer placement and Results caveats.",
        epilog="Example: python scripts/argument_screen.py DRAFT.md",
    )
    parser.add_argument("manuscript", type=Path, help="Markdown draft to screen")
    args = parser.parse_args(argv)
    if not args.manuscript.is_file():
        print(f"error: no such file: {args.manuscript}", file=sys.stderr)
        return 2
    return run(args.manuscript)


if __name__ == "__main__":
    raise SystemExit(main())
