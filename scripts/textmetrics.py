#!/usr/bin/env python3
"""
textmetrics.py -- evidence-gathering for a McEnerney-style writing review.

Pure standard library. No installation, no network.

    python3 textmetrics.py draft.md
    cat draft.txt | python3 textmetrics.py
    python3 textmetrics.py draft.md --section-from "Introduction" --section-to "Methods"

Every number here is a PROMPT FOR JUDGMENT, not a verdict. Densities are per 1,000 words so
sections of different lengths can be compared. A near-zero instability score is fatal in an
introduction and correct in a methods section. Read the text.
"""

import argparse
import re
import sys
from collections import Counter

# ---------------------------------------------------------------- lexicons

INSTABILITY = [
    "but", "however", "yet", "although", "though", "nevertheless", "nonetheless",
    "whereas", "despite", "in contrast", "by contrast", "on the contrary",
    "surprising", "surprisingly", "puzzling", "puzzle", "anomaly", "anomalous",
    "paradox", "paradoxical", "tension", "inconsistent", "inconsistency",
    "contradiction", "contradicts", "contradictory", "conflicting", "at odds",
    "fails to", "fail to", "failed to", "cannot account", "does not account",
    "unable to explain", "unexplained", "overlooked", "neglected", "unresolved",
    "problematic", "counterintuitive", "counterexample", "challenges", "undermines",
    "casts doubt", "calls into question", "misleading", "mistaken", "breaks down",
]

COST = [
    "at stake", "stakes", "consequence", "consequences", "otherwise", "unless",
    "risk", "risks", "cost", "costs", "we cannot", "we lose", "misdiagnose",
    "misallocate", "rests on", "depends on", "undermines", "implication",
    "implications", "leads us to", "would follow", "invalidates", "jeopardize",
]

CHEAP_IMPORTANCE = [
    "important", "importantly", "significant", "significantly", "crucial",
    "crucially", "critical", "essential", "key", "central", "vital", "fundamental",
    "interesting", "noteworthy", "valuable", "relevant",
]

TOPIC_VERBS = [
    "examines", "explores", "discusses", "describes", "investigates", "looks at",
    "presents", "considers", "addresses", "reviews", "surveys", "analyzes",
    "analyses", "focuses on", "deals with", "sheds light", "provides an overview",
    "aims to", "seeks to", "attempts to", "sets out to",
]

CLAIM_VERBS = [
    "argue", "argues", "show", "shows", "demonstrate", "demonstrates", "challenge",
    "challenges", "revise", "revises", "complicate", "complicates", "overturn",
    "overturns", "prove", "proves", "establish", "establishes", "explain why",
    "contend", "contends", "reject", "rejects", "refute", "refutes",
]

SCHOOL_OPENERS = [
    "in recent years", "in recent decades", "over the past", "has become increasingly",
    "have become increasingly", "growing interest", "increasing interest",
    "increasing attention", "much attention has been", "it is well known",
    "it is widely known", "throughout history", "since the dawn", "in today's world",
    "in modern society", "plays an important role", "play an important role",
    "plays a crucial role", "has long been a subject", "little attention has been",
    "few studies have", "there is a gap", "gap in the literature",
    "this paper is about", "the purpose of this paper", "the aim of this paper",
    "the goal of this paper", "in this essay", "i will discuss", "i will describe",
    "i am interested in", "this paper is organized as follows",
]

HEDGES = [
    "may", "might", "could", "perhaps", "possibly", "potentially", "somewhat",
    "relatively", "arguably", "seems", "seem", "appears", "appear", "suggests",
    "suggest", "tend to", "tends to", "in some cases", "to some extent",
    "it is possible", "likely", "unlikely", "generally", "typically", "often",
    "rather", "quite", "fairly", "presumably", "conceivably",
]

THROAT_CLEARING = [
    "it is important to note", "it should be noted", "it is worth noting",
    "it is interesting to", "it must be emphasized", "it should be emphasized",
    "it is clear that", "there are several", "there is a number of",
    "there are a number of", "the fact that", "in order to", "it can be seen that",
    "as mentioned above", "as discussed above", "as we have seen", "needless to say",
    "it goes without saying",
]

ADDITIVE_OPENERS = [
    "additionally", "furthermore", "moreover", "another", "also", "in addition",
    "similarly", "likewise", "second", "third", "finally", "next",
]

NOMINALIZATION_SUFFIXES = ("tion", "sion", "ment", "ance", "ence", "ity", "ness", "ism")
NOMINALIZATION_EXCEPTIONS = {
    "moment", "element", "argument", "document", "instrument", "environment",
    "government", "development", "experiment", "comment", "segment", "component",
    "business", "witness", "illness", "city", "community", "university", "quality",
    "quantity", "ability", "activity", "security", "society", "majority", "minority",
    "identity", "entity", "density", "capacity", "utility", "facility", "variety",
    "authority", "equity", "policy", "mechanism", "organism", "question", "section",
    "condition", "position", "function", "population", "region", "nation", "station",
    "solution", "portion", "version", "option", "relation", "tradition", "profession",
}

IRREGULAR_PARTICIPLES = {
    "made", "given", "taken", "seen", "shown", "found", "known", "held", "done",
    "written", "built", "drawn", "kept", "left", "put", "set", "sent", "brought",
    "thought", "told", "understood", "chosen", "driven", "grown",
}

BE_FORMS = {"is", "are", "was", "were", "be", "been", "being", "am"}


# ---------------------------------------------------------------- utilities

ABBREVIATIONS = {
    "e.g", "i.e", "cf", "et al", "al", "vs", "fig", "eq", "no", "ch", "pp", "p",
    "dr", "prof", "mr", "mrs", "ms", "st", "approx", "ca", "ibid",
}


def read_input(path):
    if path and path != "-":
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return sys.stdin.read()


def slice_section(text, start, end):
    lowered = text.lower()
    i = lowered.find(start.lower()) if start else 0
    if i == -1:
        sys.stderr.write(f"warning: section start {start!r} not found; using whole text\n")
        i = 0
    j = lowered.find(end.lower(), i + 1) if end else len(text)
    if j == -1:
        sys.stderr.write(f"warning: section end {end!r} not found; using to end of text\n")
        j = len(text)
    return text[i:j]


def split_paragraphs(text):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return [p for p in paras if not re.fullmatch(r"#+\s*.*", p.strip())]


def parse_sections(text):
    """{heading: body}, accepting both `**Bold**` and `## Markdown` headings.

    This is the single parser for the bundle. Three scripts each grew their own heading detection
    and two recognised only one spelling, so a draft written with bold headings was silently
    measured as having no Abstract, no Introduction and no Discussion: section word counts of 0
    that then passed every limit. A check reporting 0 words for a section it could not find is
    worse than no check, because it reads as a pass.

    Import this rather than writing another regex.
    """
    import re as _re
    pat = _re.compile(
        r"(?m)^(?:\*\*([A-Z][A-Za-z /&'\u2019-]{2,45})\*\*"
        r"|#{1,6}\s*([A-Z][A-Za-z /&'\u2019:-]{2,60}))\s*:?\s*$"
    )
    marks = [(m.start(), (m.group(1) or m.group(2)).strip().lower(), m.end())
             for m in pat.finditer(text)]
    out = {}
    for i, (_p, name, head_end) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        out.setdefault(name, text[head_end:end])
    return out


def prose_words(text):
    """Word count with table rows, code spans and link targets removed.

    The venue counts prose. A table row is columns of numbers, not a sentence, and counting those
    inflates an abstract by several words.
    """
    import re as _re
    body = _re.sub(r"(?m)^\s*\|.*$", " ", text)
    body = _re.sub(r"`[^`]*`", " ", body)
    body = _re.sub(r"\[[^\]]*\]\([^)]*\)", " ", body)
    return len([w for w in _re.split(r"\s+", body)
                if _re.search(r"[A-Za-z0-9\u00c0-\u024f]", w)])


def strip_headings(text):
    """Remove markdown headings so they don't get glued onto the following sentence."""
    return "\n".join(
        "" if re.fullmatch(r"\s*#{1,6}\s+.*", line) else line
        for line in text.splitlines()
    )


def split_sentences(text):
    """Regex sentence splitter with abbreviation guarding. Approximate by design."""
    text = re.sub(r"\s+", " ", strip_headings(text).strip())
    if not text:
        return []
    candidates = re.split(r"(?<=[.!?])[\"')\]]*\s+", text)
    sentences, buffer = [], ""
    for chunk in candidates:
        buffer = (buffer + " " + chunk).strip() if buffer else chunk
        tail = re.sub(r"[^A-Za-z.]", "", buffer.split(" ")[-1]).lower().rstrip(".")
        if tail in ABBREVIATIONS or re.fullmatch(r"[A-Za-z]", tail):
            continue
        sentences.append(buffer)
        buffer = ""
    if buffer:
        sentences.append(buffer)
    return [s for s in sentences if s.strip()]


def words(text):
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text)


def count_phrases(text_lower, phrases):
    """Count phrase occurrences; single words matched on word boundaries."""
    hits = Counter()
    for phrase in phrases:
        pattern = r"\b" + re.escape(phrase) + (r"\b" if phrase.isalpha() else "")
        n = len(re.findall(pattern, text_lower))
        if n:
            hits[phrase] = n
    return hits


def per_k(count, total_words):
    return (count * 1000.0 / total_words) if total_words else 0.0


def find_sentences_with(sentences, phrases, limit=4):
    out = []
    for s in sentences:
        low = s.lower()
        for phrase in phrases:
            pattern = r"\b" + re.escape(phrase) + (r"\b" if phrase.isalpha() else "")
            if re.search(pattern, low):
                out.append((phrase, s))
                break
        if len(out) >= limit:
            break
    return out


def truncate(s, n=150):
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def nominalizations(word_list):
    hits = Counter()
    for w in word_list:
        lw = w.lower()
        if len(lw) < 7 or lw in NOMINALIZATION_EXCEPTIONS:
            continue
        base = lw[:-1] if lw.endswith("s") and not lw.endswith("ss") else lw
        if base in NOMINALIZATION_EXCEPTIONS:
            continue
        if base.endswith(NOMINALIZATION_SUFFIXES):
            hits[base] += 1
    return hits


def passive_count(sentences):
    total, examples = 0, []
    pattern = re.compile(
        r"\b(is|are|was|were|be|been|being|am)\b\s+(?:\w+ly\s+)?(\w+)", re.I
    )
    for s in sentences:
        found = False
        for m in pattern.finditer(s):
            cand = m.group(2).lower()
            if cand.endswith("ed") or cand in IRREGULAR_PARTICIPLES:
                total += 1
                found = True
        if found and len(examples) < 3:
            examples.append(s)
    return total, examples


AUXILIARIES = BE_FORMS | {
    "has", "have", "had", "do", "does", "did", "can", "could", "will", "would",
    "shall", "should", "must", "may", "might",
}


def aux_position(sentence):
    """Index of the first auxiliary/be verb, if any.

    Deliberately conservative: it only finds auxiliaries, not lexical verbs, so treat a
    large value as a hint to read the sentence rather than as proof of a delayed verb.
    """
    for i, t in enumerate(words(sentence)):
        if t.lower() in AUXILIARIES:
            return i
    return None


def opening_clause_length(sentence):
    """Words before the first comma -- a proxy for how long the reader waits."""
    head = sentence.split(",")[0]
    return len(words(head)) if "," in sentence else len(words(sentence))


# ---------------------------------------------------------------- report

def bar(value, scale=2.0, width=28):
    n = min(width, int(round(value / scale)))
    return "#" * n if n else "."


def section(title):
    return f"\n{title}\n{'-' * len(title)}"


def analyze(text, top_n=8, focus="all"):
    """focus: 'all' | 'sentences' | 'argument'.

    The split exists because two different jobs read this output. An argument review asks
    whether anything is at risk for the reader and whether the text moves; a line-level
    clarity pass asks whether each sentence is shaped the way readers process English.
    Feeding either job the other's numbers invites the reviewer to drift off task.
    """
    arg = focus in ("all", "argument")
    sen = focus in ("all", "sentences")

    out = []
    paragraphs = split_paragraphs(text)
    sentences = split_sentences(text)
    all_words = words(text)
    wc = len(all_words)
    lower = text.lower()
    n = [0]

    def head(title):
        n[0] += 1
        out.append(section(f"{n[0]}. {title}"))

    def report(label, phrases, note):
        hits = count_phrases(lower, phrases)
        total = sum(hits.values())
        d = per_k(total, wc)
        out.append(f"  {label:<24} {total:>4}  ({d:5.1f}/1k)  {bar(d)}")
        if hits:
            top = ", ".join(f"{w}\u00d7{c}" for w, c in hits.most_common(top_n))
            out.append(f"    {top}")
        out.append(f"    -> {note}")
        return total, hits

    out.append("=" * 72)
    label = {"all": "", "sentences": "  [sentence focus]", "argument": "  [argument focus]"}[focus]
    out.append("TEXT METRICS -- evidence for judgment, not a score" + label)
    out.append("=" * 72)

    # ------------------------------------------------------------------ shape
    if sen:
        head("SHAPE")
        lengths = [len(words(s)) for s in sentences] or [0]
        mean_len = sum(lengths) / len(lengths)
        out.append(f"  words {wc} | sentences {len(sentences)} | paragraphs {len(paragraphs)}")
        out.append(f"  mean sentence {mean_len:.1f} words | "
                   f"shortest {min(lengths)} | longest {max(lengths)}")
        short = sum(1 for l in lengths if l <= 12)
        long_ = sum(1 for l in lengths if l >= 35)
        out.append(f"  sentences <=12 words: {short} ({per_k(short, len(sentences)) / 10:.0f}%) | "
                   f">=35 words: {long_} ({per_k(long_, len(sentences)) / 10:.0f}%)")
        out.append("  NOTE: variance matters more than the mean. No short sentences means no "
                   "claim ever lands hard.")
        longest = sorted(sentences, key=lambda s: -len(words(s)))[:3]
        if longest:
            out.append("  longest sentences:")
            for s in longest:
                out.append(f"    [{len(words(s))}w] {truncate(s)}")

        delayed = [(aux_position(s), s) for s in sentences]
        delayed = [(p, s) for p, s in delayed if p is not None and p >= 12]
        heavy = [(opening_clause_length(s), s) for s in sentences]
        heavy = [(k, s) for k, s in heavy if k >= 15]
        out.append(f"  sentences with a 15+ word opening clause: {len(heavy)}  "
                   f"| first auxiliary after word 12: {len(delayed)}")
        out.append("    -> Readers hold everything before the verb in suspense. Long openings "
                   "delay judgment.")
        for k, s in sorted(heavy, reverse=True)[:3]:
            out.append(f"    [{k}w before break] {truncate(s)}")

    # -------------------------------------------------------- value / stakes
    if arg:
        head("VALUE AND STAKES SIGNALS (per 1,000 words)")
        inst_total, _ = report(
            "instability markers", INSTABILITY,
            "Is anything the reader believes put at risk? Expected high in intro/discussion, "
            "near zero in methods.")
        cost_total, _ = report(
            "cost / stakes language", COST,
            "Does the draft say what is lost if this stays unresolved? This is the step writers "
            "skip.")
        cheap_total, _ = report(
            "cheap importance words", CHEAP_IMPORTANCE,
            "These ASSERT value. High count with low cost-language usually means stakes were "
            "never worked out.")
        report("topic verbs", TOPIC_VERBS,
               "'examines/explores/discusses' describe activity, not change. Compare with claim "
               "verbs below.")
        report("claim verbs", CLAIM_VERBS,
               "'argues/shows/challenges' commit to changing a belief. Ratio to topic verbs is "
               "the tell.")
        if inst_total and cost_total == 0:
            out.append("  !! FLAG: instability present, cost language absent. A problem with no "
                       "consequences gives no reason to care.")
        if cheap_total > 2 * max(cost_total, 1):
            out.append("  !! FLAG: importance is asserted far more than it is demonstrated.")

    # ------------------------------------------------------- wasted openings
    if sen:
        head("WASTED WORDS (per 1,000 words)")
        report("school-writing openers", SCHOOL_OPENERS,
               "Habits from writing for a paid reader. Each one spends attention on nothing.")
        report("hedges", HEDGES,
               "Field-dependent. Look for STACKING (2+ in one sentence) rather than raw count.")
        report("throat-clearing", THROAT_CLEARING,
               "Consumes the sentence opening -- the highest-attention position -- with no "
               "content.")
        stacked = []
        for s in sentences:
            low = s.lower()
            k = sum(1 for h in HEDGES if re.search(r"\b" + re.escape(h) + r"\b", low))
            if k >= 3:
                stacked.append((k, s))
        if stacked:
            out.append(f"  hedge stacks (3+ in one sentence): {len(stacked)}")
            for k, s in sorted(stacked, reverse=True)[:3]:
                out.append(f"    [{k} hedges] {truncate(s)}")

    # ------------------------------------------------------ agency/abstraction
    if sen:
        head("AGENCY AND ABSTRACTION")
        noms = nominalizations(all_words)
        nom_total = sum(noms.values())
        out.append(f"  nominalizations {nom_total} ({per_k(nom_total, wc):.1f}/1k)  "
                   f"{bar(per_k(nom_total, wc))}")
        if noms:
            out.append("    " + ", ".join(f"{w}\u00d7{c}" for w, c in noms.most_common(top_n)))
        out.append("    -> Actions hidden inside nouns. Some are legitimate technical terms; "
                   "clusters are where readers lose the actors.")
        p_total, p_ex = passive_count(sentences)
        out.append(f"  probable passives {p_total} ({per_k(p_total, wc):.1f}/1k)")
        out.append("    -> Passive is NOT an error. Flag only where it hides an agent the reader "
                   "needs -- especially when the hidden agent is the author.")
        for s in p_ex:
            out.append(f"    {truncate(s)}")

    # ----------------------------------------------------------- cohesion
    sent_additive = [s for s in sentences
                     if words(s) and words(s)[0].lower() in ADDITIVE_OPENERS]
    if arg:
        head("MOVEMENT (paragraph-opening topic string)")
        out.append("  Read this list alone. Does it advance an argument, or inventory topics?")
        additive = 0
        for i, p in enumerate(paragraphs, 1):
            opening = " ".join(words(p)[:7])
            first_word = words(p)[0].lower() if words(p) else ""
            mark = ""
            if first_word in ADDITIVE_OPENERS:
                additive += 1
                mark = "  <- additive: announces accumulation, not development"
            out.append(f"   {i:>3}. {opening}\u2026{mark}")
        out.append(f"\n  paragraphs opening with an additive connector: "
                   f"{additive}/{len(paragraphs)}")
        out.append(f"  sentences opening with an additive connector: "
                   f"{len(sent_additive)}/{len(sentences)}")
        out.append("    -> Additive connectors announce that another item is coming. Logical "
                   "connectors (but, because, so, which is why) say what relation it bears.")
        for s in sent_additive[:3]:
            out.append(f"    {truncate(s, 110)}")
    elif sen:
        head("COHESION")
        out.append(f"  sentences opening with an additive connector: "
                   f"{len(sent_additive)}/{len(sentences)}")
        out.append("    -> Additive connectors (also, moreover, furthermore) announce that "
                   "another item is coming. Logical connectors (but, because, so, which is why) "
                   "say what relation it bears.")
        for s in sent_additive[:3]:
            out.append(f"    {truncate(s, 110)}")
        out.append("  paragraph-opening subjects (first 7 words) -- do consecutive paragraphs "
                   "share a topic?")
        for i, p in enumerate(paragraphs[:15], 1):
            out.append(f"   {i:>3}. {' '.join(words(p)[:7])}\u2026")

    # --------------------------------------------- where instability appears
    if arg:
        head("WHERE SOMETHING FIRST GOES WRONG")
        first_hit = None
        for i, p in enumerate(paragraphs, 1):
            if count_phrases(p.lower(), INSTABILITY):
                first_hit = i
                break
        if first_hit is None:
            out.append("  No instability marker found anywhere. If this is an introduction, "
                       "abstract, or discussion, that is the headline finding.")
        else:
            out.append(f"  First instability marker appears in paragraph {first_hit} "
                       f"of {len(paragraphs)}.")
            out.append("  -> If that number is greater than 1 or 2, ask why the paper doesn't "
                       "start there.")
        ex = find_sentences_with(sentences, INSTABILITY, limit=4)
        for phrase, s in ex:
            out.append(f"    [{phrase}] {truncate(s)}")

    # ------------------------------------------------------ stress positions
    if sen:
        head("STRESS POSITIONS (last 4 words of each sentence)")
        out.append("  This is what your reader carries forward. Citations and 'in this context' "
                   "waste it.")
        tails = []
        for s in sentences[:40]:
            w = re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", s)
            if w:
                tails.append(" ".join(w[-4:]))
        for t in tails[:25]:
            out.append(f"    \u2026 {t}")
        if len(tails) > 25:
            out.append(f"    (+{len(tails) - 25} more)")

    out.append("\n" + "=" * 72)
    out.append("Reminder: every number above is a question, not an answer. Interpret against "
               "the section's job and the venue's conventions.")
    out.append("=" * 72)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default="-", help="file to analyze, or - for stdin")
    ap.add_argument("--section-from", default=None,
                    help="analyze only from this heading/phrase onward")
    ap.add_argument("--section-to", default=None, help="stop at this heading/phrase")
    ap.add_argument("--top", type=int, default=8, help="how many top terms to list")
    ap.add_argument("--focus", choices=["all", "sentences", "argument"], default="all",
                    help="which layer of evidence to print (default: all)")
    args = ap.parse_args()

    # Don't traceback when piped into head/less.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass

    text = read_input(args.path)
    if args.section_from or args.section_to:
        text = slice_section(text, args.section_from, args.section_to)
    if not text.strip():
        sys.exit("No text to analyze.")
    print(analyze(text, top_n=args.top, focus=args.focus))


if __name__ == "__main__":
    main()
