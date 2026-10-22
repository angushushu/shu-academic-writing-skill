#!/usr/bin/env python3
"""Ingestion screen: what stops a submission before anyone reads the science.

Pass 1 of the two-pass audit. This is a **gate, not a screen among several** — if it flags
anything, the audit halts with `intake_rejected` and the review lanes never run. That is the
point: a missing table and an unsupported causal claim are not comparable risks, and grading
them on one ladder is a category error.

It is deliberately dumb. It uses regexes, header structure, and arithmetic, and it makes no
judgement about meaning. Everything it cannot see is Pass 2's job, so a clean run here proves
nothing about the paper.

Stdlib only. Cross-platform. `--help` works.

Usage:
    python scripts/intake_screen.py DRAFT.md
    python scripts/intake_screen.py DRAFT.md --profile project/venue-target.md
    python scripts/intake_screen.py DRAFT.md --json

Exit codes:
    0  clean — proceed to Pass 2
    1  intake defects found — halt, verdict is intake_rejected
    2  could not run (missing file, unreadable profile)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --- what counts as an intake blocker ---------------------------------------
# `(Author, year)` is the default unresolved placeholder emitted by every reference manager
# (EndNote, Zotero, Word's own citation tool). Leaving it out of this list -- as an earlier
# version did, hardcoding only REF/CITATION/TODO/TBD -- made Pass 1 blind to the single most
# common unresolved citation in real drafts. Reported by T5b, verified against ms-03.md.
PLACEHOLDER_PATTERNS = [
    ("citation placeholder", re.compile(r"\((?:REF|ref|CITATION|citation|TODO|TBD)\b[^)]*\)")),
    ("citation placeholder", re.compile(r"\(\s*Author,?\s*(?:year|YEAR|date)\s*\)")),
    ("citation placeholder", re.compile(r"\(\s*[A-Z][a-z]+ et al\.,?\s*(?:year|YEAR|n\.d\.)\s*\)")),
    ("citation placeholder", re.compile(r"\[\s*(?:citation|ref|reference)\s+(?:needed|required)\s*\]", re.I)),
    ("drafting markup", re.compile(r"\[\[\s*[^\]]{3,90}\]\]")),
    ("drafting markup", re.compile(r"<(?:Table|Figure|Fig\.?|TABLE|FIGURE)\s+[\w.]+\s+here\s*>", re.I)),
    ("drafting markup", re.compile(r"\{\{[^}]{3,90}\}\}")),
    ("drafting tag", re.compile(r"\b(?:TODO|FIXME|TBD|XXX)\b\s*:?", re.I)),
    # Single-bracket editorial markers left in headings or body: `[RQ1]`, `[H2]`, `[exploratory]`.
    #
    # Added after a revision written WITH this bundle's own method was marked down by judges for
    # leaving four of these in Results headings, while this screen reported CLEAN. The screen knew
    # `[[...]]`, `(REF)`, `<Table N here>` and bare `TODO`, and knew nothing about the marker family
    # a writer annotating their own draft actually uses. A gate that misses the marks produced by
    # the workflow it guards is the least useful kind there is.
    #
    # Deliberately narrow: `[1]`, `[Smith, 2020]` and `[see section 2]` are citations and
    # cross-references, not drafting tags, and flagging them would halt real manuscripts.
    ("drafting tag", re.compile(
        r"\[\s*(?:RQ\s*\d+|[Hh]\d+|[Ee]xploratory|[Cc]onfirmatory|[Pp]ilot|[Dd]raft)\s*\]")),
]

# A planning note in square brackets, e.g. "[why this matters - to fill in]". Kept separate
# because it needs care: real prose uses brackets for citations and asides.
SQUARE_NOTE = re.compile(r"\[(?!\d)([^\]\n]{6,120})\]")

NOTE_CUES = re.compile(
    r"to fill in|fill in|to be added|add (?:this|here)|insert |placeholder|"
    r"rewrite|reword|check |verify |expand|tbd|todo|note to self|\bwhy this\b|\bexpand here\b",
    re.I,
)

REQUIRED_SECTIONS = [
    "Research Transparency Statement",
    "Transparency Statement",
    "Data Availability",
    "Ethics",
    "Limitations",
]

REFS_HEADING = re.compile(
    # Accepts `References`, `**References**`, `## References`, `### References` and
    # `7. References`. The first version accepted only the first two, so a manuscript that
    # used a Markdown heading was rejected for "no reference list" while its list sat right
    # there -- a false BLOCKER, which halts the audit outright. Fifth instance of the same
    # heading-format assumption in this bundle; see textmetrics.parse_sections for the fix
    # that made it a shared function.
    r"^\s*(?:#{1,6}\s*)?(?:\d+\.?\s*)?\**\s*(References|Bibliography|Works Cited)\s*\**\s*:?\s*$",
    re.I | re.M,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def strip_noise(text: str) -> str:
    """Remove things that look like markup but are legitimate."""
    t = re.sub(r"```.*?```", "", text, flags=re.S)          # fenced code
    t = re.sub(r"`[^`\n]+`", "", t)                          # inline code
    t = re.sub(r"\$[^$\n]+\$", "", t)                        # math
    t = re.sub(r"\((?:19|20)\d\d[a-z]?\)", "", t)            # (2020) year citations
    t = re.sub(r"\((?:[A-Z][\w'.-]+(?: (?:&|and) [A-Z][\w'.-]+)?,? \d{4}[a-z]?)\)", "", t)
    return t


def find_placeholders(text: str) -> list[dict]:
    out = []
    clean = strip_noise(text)
    for label, rx in PLACEHOLDER_PATTERNS:
        for m in rx.finditer(clean):
            out.append({"kind": label, "match": m.group(0)[:80], "index": m.start()})
    # Angle-bracket placeholders in prose: `<character's name>`, `<insert effect size>`.
    #
    # Added after a blind judge found `<character's name>` sitting in a delivered revision while
    # this screen reported CLEAN. The screen knew `<Table N here>` and stopped there, so the whole
    # family of "leave a slot for the author" placeholders went unseen.
    #
    # Distinguished from HTML by content, not by tag name: legitimate markup like `<sub>`, `</sub>`
    # and `<br/>` has no space and no apostrophe inside, while a prose placeholder almost always has
    # one. Flagging `<sub>` would make every formula-bearing manuscript fail intake, which is a
    # worse error than the one being fixed.
    for m in re.finditer(r"<([^<>\n]{2,60})>", clean):
        inner = m.group(1)
        if inner.startswith(("/", "http", "www")):
            continue
        if " " not in inner and "'" not in inner and "\u2019" not in inner:
            continue
        out.append({"kind": "drafting markup", "match": m.group(0)[:80], "index": m.start()})

    for m in SQUARE_NOTE.finditer(clean):
        inner = m.group(1)
        if NOTE_CUES.search(inner):
            out.append({"kind": "planning note", "match": m.group(0)[:80], "index": m.start()})
    # de-duplicate by position
    seen, uniq = set(), []
    for h in sorted(out, key=lambda x: x["index"]):
        if h["index"] in seen:
            continue
        seen.add(h["index"])
        uniq.append(h)
    return uniq


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def empty_required_sections(text: str) -> list[dict]:
    """A mandatory section present as a heading with no content under it."""
    out = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        raw = line.strip()
        if not raw or len(raw) > 90:
            continue
        heading = None
        m = re.match(r"^\s*(?:\*\*|#{1,6}\s*)?([A-Z][A-Za-z ’'\-]{3,60})\s*(?:\*\*)?\s*:?\s*$", raw)
        if m:
            heading = m.group(1).strip()
        else:
            m2 = re.match(r"^\s*#{1,6}\s+(.{3,60})$", raw)
            if m2:
                heading = m2.group(1).strip()
        if not heading:
            continue
        if not any(heading.lower() == s.lower() for s in REQUIRED_SECTIONS):
            continue
        body = []
        for j in range(i + 1, min(i + 8, len(lines))):
            nxt = lines[j].strip()
            if re.match(r"^(?:\*\*|#{1,6}\s)", nxt) and not nxt.startswith("**"):
                break
            if re.match(r"^\*\*[^*]+\*\*\s*$", nxt):
                break
            body.append(nxt)
        if not any(b for b in body):
            out.append({"kind": "empty required section", "section": heading, "line": i + 1})
    return out


def missing_references(text: str) -> list[dict]:
    """In-text citations with no reference list anywhere in the document.

    BLOCKING, not advisory. T5b corrected an earlier version of this function, which argued that
    a broken citation is fixable and therefore not an intake failure. That confused two different
    things: an *unresolvable* citation (citing an unindexed source, wrong year) is a Pass 2
    concern, but a document that cites sources and contains no `References`, `Bibliography`, or
    `Works Cited` heading at all is structurally incomplete and is returned at the editorial desk
    by every journal that screens for required components. The distinction is between a defect in
    the scholarship and a missing required part of the submission.
    """
    has_list = bool(REFS_HEADING.search(text))
    cites = re.findall(r"\(([A-Z][A-Za-z'.-]+(?: (?:&|and) [A-Z][A-Za-z'.-]+)?,\s*\d{4}[a-z]?)\)", text)
    if cites and not has_list:
        return [{"kind": "no reference list",
                 "detail": f"{len(cites)} in-text citation(s) but no References heading",
                 "examples": cites[:4]}]
    return []


def split_for_audit(text: str) -> tuple[str, str]:
    """Return (body_without_references, references_section).

    Exists because the case builder trimmed the reference list off the end of the manuscript and
    then the screen reported "no reference list" -- a blocker it had created itself. A screen must
    be shown the whole document, or it will manufacture exactly the defect it looks for.
    """
    m = REFS_HEADING.search(text)
    if not m:
        return text, ""
    return text[: m.start()].rstrip(), text[m.start():].strip()


def unmatched_table_refs(text: str) -> list[dict]:
    """A placeholder tag standing in for an asset that was never inserted.

    NARROW ON PURPOSE, and this is the important part. An earlier version compared every
    `Table N` mention in the prose against captions and reported any mismatch as a missing
    asset. On the synthetic specimens that looked correct. On a real published paper extracted
    from PDF it produced **five false blockers in one pass** -- `Table 1`, and Tables 7-11 --
    because a paper cites its tables in prose ("...and Table 7 shows the correlation") and the
    caption may sit elsewhere, in a different style, or be laid out after the table body.

    A mechanical screen cannot tell whether some `Table 7` exists in the submission. It can only
    see an explicit placeholder saying it does not. So that is all this checks. A prose mention
    with no visible caption is reported separately as an advisory, for Pass 2 to resolve.
    """
    out = []
    for m in re.finditer(r"<(?:Table|Figure|Fig\.?|TABLE|FIGURE)\s+([\w.]+)\s+here\s*>", text, re.I):
        out.append({"kind": "referenced but absent", "asset": f"Table/Figure {m.group(1)}",
                    "match": m.group(0)[:60]})
    return out


def uncaptioned_asset_mentions(text: str) -> list[dict]:
    """Assets cited in prose with no caption visible in the text. ADVISORY.

    Not a blocker: PDF extraction, separate attachment, and supplementary placement all make a
    missing caption a poor signal about whether the asset exists.
    """
    cited = set(re.findall(r"\b(?:Table|Figure|Fig\.)\s+(\d+)\b", text))
    captioned = set()
    for m in re.finditer(r"\b(?:Table|Figure|Fig\.)\s+(\d+)\b([^\n]{0,60})", text):
        tail = m.group(2).strip()
        if re.match(r"^(?:[:.—-]|\s)(?:presents|shows|reports|summarises|summarizes|lists|"
                    r"gives|details|provides)", tail, re.I):
            captioned.add(m.group(1))
    captioned |= set(re.findall(r"(?m)^\s*\**\s*(?:Table|Figure|Fig\.)\s+(\d+)\s*[:.—-]", text))
    missing = sorted(cited - captioned, key=lambda x: int(x))
    if not missing:
        return []
    return [{"kind": "asset not visible in text",
             "detail": f"cited but no caption found for: "
                       f"{', '.join('Table/Figure ' + m for m in missing[:8])}",
             "caveat": "may be an attachment or supplementary; verify in Pass 2"}]


def unreported_placeholders(text: str) -> list[dict]:
    """Deprecated shim. Kept so an older caller does not silently lose the check."""
    return missing_references(text)


def _sections(text: str) -> dict[str, str]:
    """Split on `**Bold**` or `## Markdown` headings.

    Both forms must be recognised. The first version handled only the bold form, so a manuscript
    written with `## Abstract` produced an empty Abstract section and its word count of 0 passed the
    venue's 150-word limit without being measured. A gate that silently skips a check because it did
    not recognise a heading is worse than no gate: it reports CLEAN.
    """
    pat = re.compile(
        r"(?m)^(?:\*\*([A-Z][A-Za-z /&'\u2019-]{2,40})\*\*"
        r"|#{1,4}\s+([A-Z][A-Za-z /&'\u2019:-]{2,60}))\s*$"
    )
    marks = [(m.start(), (m.group(1) or m.group(2)).strip(), m.end()) for m in pat.finditer(text)]
    out: dict[str, str] = {}
    for i, (_pos, name, head_end) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        out.setdefault(name, text[head_end:end].strip())
    return out


def venue_word_limits(text: str, limits: dict, override: int | None = None) -> list[dict]:
    """Check the venue's limits against the sections they actually apply to.

    An earlier version took `front_back_max_words` and measured the WHOLE manuscript against it,
    reporting a 4,616-word paper as 2,616 words over a 2,000-word limit. That is not a stricter
    check, it is a wrong one, and a gate that halts every submission is the failure mode this
    module's own warning describes. The venue's limits are section-scoped:

        abstract_max_words           -> the Abstract only
        front_back_max_words         -> Introduction + Discussion + footnotes + ack + appendices
        method_results_target_words  -> Method + Results, advisory ("approximately"), never halts

    `override` keeps whole-document behaviour available explicitly, via --max-words.
    """
    out: list[dict] = []

    def words(s: str) -> int:
        body = re.sub(r"(?m)^\s*\|.*$", "", s)
        return len([w for w in re.split(r"\s+", body) if re.search(r"[A-Za-z0-9]", w)])

    if override is not None and override > 0:
        n = words(text)
        if n > override:
            out.append({"kind": "word ceiling exceeded", "scope": "whole document",
                        "count": n, "limit": override, "over": n - override})
        return out

    sec = _sections(text)

    def section_words(*names: str) -> int:
        return sum(words(v) for k, v in sec.items()
                   if any(n.lower() in k.lower() for n in names))

    ab = limits.get("abstract_max_words", -1)
    if ab and ab > 0:
        n = section_words("abstract")
        if n > ab:
            out.append({"kind": "word ceiling exceeded", "scope": "abstract",
                        "count": n, "limit": ab, "over": n - ab})

    fb = limits.get("front_back_max_words", -1)
    if fb and fb > 0:
        n = section_words("introduction", "discussion", "acknowledg", "appendix", "footnote")
        if n > fb:
            out.append({"kind": "word ceiling exceeded",
                        "scope": "Introduction + Discussion + notes",
                        "count": n, "limit": fb, "over": n - fb})

    return out


def parse_profile_limits(profile: Path) -> dict:
    if not profile or not profile.is_file():
        return {}
    t = read(profile)
    block = re.search(r"```limits\n(.*?)```", t, re.S)
    if not block:
        return {}
    out = {}
    for line in block.group(1).strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            try:
                out[k.strip()] = int(v.strip())
            except ValueError:
                pass
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manuscript")
    ap.add_argument("--profile", help="venue-target.md with a ```limits block")
    ap.add_argument("--max-words", type=int, default=None,
                    help="override the venue's total word ceiling")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    p = Path(a.manuscript)
    if not p.is_file():
        print(f"cannot read {p}", file=sys.stderr)
        return 2
    text = read(p)

    limits = parse_profile_limits(Path(a.profile)) if a.profile else {}

    # Kinds that halt intake. These are the ones a venue screens mechanically, and the ones that
    # cannot be fixed while the science stands.
    #
    # `no reference list` and `referenced but absent` are BLOCKERS. An earlier version treated
    # them as advisories, on the reasoning that a gate firing on every imperfection never opens.
    # That reasoning was half right and led to two errors, both caught by T5b:
    #   - a document citing sources with no bibliography is structurally incomplete and is
    #     returned at the editorial desk, so it is an intake failure, not a scholarly one;
    #   - but "advisory" as a category is still needed, because a manuscript can be ingestible
    #     while carrying defects that Pass 2 must examine.
    # The category stays; these two checks moved out of it.
    BLOCKING_KINDS = {
        "citation placeholder", "drafting markup", "drafting tag",
        "planning note", "empty required section", "referenced but absent",
        "word ceiling exceeded", "no reference list",
    }

    raw = []
    for h in find_placeholders(text):
        raw.append({**h, "line": line_of(text, h.pop("index"))})
    raw += empty_required_sections(text)
    raw += missing_references(text)
    raw += unmatched_table_refs(text)
    raw += uncaptioned_asset_mentions(text)
    raw += venue_word_limits(text, limits, a.max_words)

    blockers = [f for f in raw if f["kind"] in BLOCKING_KINDS]
    advisories = [f for f in raw if f["kind"] not in BLOCKING_KINDS]

    result = {
        "manuscript": str(p),
        "verdict": "intake_rejected" if blockers else "proceed_to_pass2",
        "blockers": blockers,
        "advisories": advisories,
        "checks_run": {
            "placeholders": True, "empty_required_sections": True,
            "reference_list": True, "unmatched_table_refs": True,
            "word_ceiling": ("whole-document override" if a.max_words is not None
                             else {k: v for k, v in limits.items() if v and v > 0} or None),
        },
        "note": (
            "A clean run proves only that no mechanical intake defect was found. It says "
            "nothing about the paper's argument, evidence, or reporting -- that is Pass 2."
        ),
    }

    if a.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if not raw:
            print(f"CLEAN — {p.name}: no intake defect and no advisory found.")
            print("  This is not a pass. Run Pass 2.")
        elif not blockers:
            print(f"PROCEED TO PASS 2 — {p.name}: no blocking intake defect.")
            print(f"  {len(advisories)} advisor{'y' if len(advisories)==1 else 'ies'} to carry "
                  f"into the review:")
            for f in advisories:
                desc = f.get("detail") or f.get("kind")
                print(f"    · [{f['kind']}] {desc}")
        else:
            print(f"INTAKE_REJECTED — {p.name}: {len(blockers)} blocking defect(s)\n")
            for f in blockers:
                loc = f" line {f['line']}" if "line" in f else ""
                desc = f.get("match") or f.get("detail") or f.get("asset") or f.get("section") or ""
                if f["kind"] == "word ceiling exceeded":
                    desc = f"{f['count']} words vs limit {f['limit']} (over by {f['over']})"
                if f["kind"] == "empty required section":
                    desc = f"'{f['section']}' present as a heading with no content"
                print(f"  [{f['kind']}]{loc}  {desc}")
            if advisories:
                print(f"\n  Plus {len(advisories)} advisor"
                      f"{'y' if len(advisories)==1 else 'ies'} (not blocking):")
                for f in advisories:
                    print(f"    · [{f['kind']}] {f.get('detail') or f['kind']}")
            print("\n  Halt. Do not run the review lanes.")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
