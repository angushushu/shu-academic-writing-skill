#!/usr/bin/env python3
"""
norms.py -- put a draft's indices on a percentile scale against a reference corpus.

This is the whole point of the exercise. "Your adjacent-sentence content-lemma overlap is
0.18" tells nobody anything. "0.18, which is the 12th percentile against 40 articles from
Discourse Processes" is evidence a writer can act on, and it is the only form in which these
indices carry meaning -- they were built as norm-referenced instruments, and reading a raw
value as if it had an absolute interpretation is the most common way people misuse them.

Two steps:

  1. Build norms from a corpus you assembled (published articles from the target venue):
       python3 norms.py build --metrics corpus_tidy.csv --out norms.json

  2. Compare a draft against them:
       python3 norms.py compare --metrics draft_tidy.csv --norms norms.json

Both --metrics files come from run_tools.py. The corpus is yours to assemble and its
composition IS the analysis: norms built from 40 papers in the author's exact target venue
say something; norms built from whatever PDFs were lying around say nothing.
"""

import argparse
import csv
import json
import math
import re
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

MIN_CORPUS = 20  # below this, percentiles are noise dressed up as precision


# Pattern -> the diagnostic question the index actually bears on. Regex rather than an exact
# allowlist because these tools rename columns between versions, and a brittle list would
# silently drop half the output after an upgrade.
RELEVANCE = [
    # ---- tier 1 (pip backends) -------------------------------------------------------
    (r"order_coherence|^coherence", "cohesion",
     "textdescriptives coherence: cosine similarity between adjacent (first-order) and "
     "once-removed (second-order) sentence embeddings. The embedding-based analogue of "
     "old-before-new. Low first-order with adequate second-order suggests interleaved "
     "topics rather than disconnection."),
    (r"dependency_distance", "sentence-density",
     "Mean dependency distance and proportion of adjacent dependencies. Long dependencies "
     "mean words that must be held in mind before their relation resolves -- the "
     "quantitative shadow of the delayed-verb diagnosis."),
    # NB: classify() lowercases the index name before matching, so these POS tags must be
    # written lowercase even though the backends emit them uppercase.
    (r"^pos_prop_(noun|propn|adj|adp)", "sentence-density",
     "Noun, proper-noun, adjective and adposition share. Elevated together is the "
     "signature of phrasal compression: content packed into noun phrases."),
    (r"^pos_prop_(verb|aux)", "agency",
     "Verb share. A low verb-to-noun ratio is where characters stop doing things."),
    (r"^pos_prop_(pron|det)", "cohesion",
     "Pronoun and determiner share. Bears on given-new management: very low pronoun use "
     "usually means full noun phrases repeated where continuity was available."),
    (r"^pos_prop_(cconj|sconj)", "movement",
     "Coordinating vs subordinating conjunction share. Subordination carries logical "
     "relation; coordination tends to accumulate."),
    (r"flesch|smog|gunning|coleman|automated_readability|^lix|^rix", "sentence-density",
     "Readability formulas. Crude -- they see only word and sentence length -- but useful "
     "as a corpus-relative baseline. Never report one as a grade level to an academic."),
    (r"sentence_length|token_length|syllables|n_tokens|n_characters", "sentence-density",
     "Length baselines. Weak alone; useful as denominators and for variance."),
    (r"^(n_|a_)(noun|adj|adp|propn)", "sentence-density",
     "lftk nominal counts and per-sentence averages. Phrasal density."),
    (r"^(n_|a_)(verb|aux)", "agency",
     "lftk verb counts. Whether actions live in verbs."),
    (r"^(n_|a_)(sconj|cconj|conj|subord|coord)", "movement",
     "lftk conjunction counts. Subordination vs coordination."),
    (r"^(mattr|mtld|mtldma|hdd|msttr|simpttr|rttr|lttr|maasttr)", "lexical-diversity",
     "taaled lexical diversity. VALIDITY WARNING: validated as a proficiency and "
     "development measure, not as a measure of value to expert readers. In expert academic "
     "prose a LOW score often reflects correct, consistent terminology. See "
     "references/index-map.md §4 before letting this shape any advice."),

    # ---- tier 2 (canonical repo tools) ------------------------------------------------
    (r"^adjacent_overlap.*(sent|para)", "cohesion",
     "Old-before-new across adjacent sentences/paragraphs. Low values mean consecutive "
     "sentences share little material, so readers have nothing to attach new content to."),
    (r"^(lsa|lda|word2vec)_[12]_all_(sent|para)", "cohesion",
     "Semantic similarity between adjacent segments. Distinguishes genuine topic development "
     "from disconnection; unlike lemma overlap it survives synonym variation."),
    (r"^syn_overlap", "cohesion",
     "Synonym-based overlap. High lemma overlap with low synonym overlap suggests repetition "
     "rather than development."),
    (r"connective|conjunct|adversative|causal|logical|temporal|additive", "movement",
     "Connective incidence by type. The additive-vs-logical ratio is the one that matters: "
     "additive connectives announce accumulation, logical ones carry an argument."),
    (r"givenness|pronoun|repeated_content", "cohesion",
     "Given-new management. Pronoun density and repeated lemmas show whether the text keeps "
     "referring back or keeps starting over."),
    (r"^(mattr|mtld|mltd|hdd|msttr|.*_ttr)", "lexical-diversity",
     "Lexical diversity. VALIDITY WARNING: validated as a proficiency and development "
     "measure, not as a measure of value to expert readers. See references/index-map.md "
     "before letting this influence any writing advice."),
    (r"nominal|nn_all|noun_phrase|^np_|premod|attrib", "sentence-density",
     "Noun-phrase elaboration. The quantitative form of the nominalization diagnosis: "
     "actions packed into noun phrases instead of verbs."),
    (r"clause|clausal|finite|complement|relative|advl|subordin", "sentence-density",
     "Clausal complexity. Distinguishes elaboration that readers process easily (clausal) "
     "from elaboration that compresses (phrasal)."),
    (r"^(mean_length|wrd_length|word_length|sent_length|.*_per_)", "sentence-density",
     "Length and density baselines."),
    (r"passive|^vb_|verb", "agency",
     "Verb and voice profile. Bears on whether characters are visible as subjects."),
]


def classify(index_name):
    low = index_name.lower()
    for pat, layer, gloss in RELEVANCE:
        if re.search(pat, low):
            return layer, gloss
    return None, None


def load_tidy(path):
    """tidy CSV -> ({(backend, index): {text: value}}, provenance)

    Provenance is the set of backends that produced the rows. It travels with the norms
    because a percentile is only meaningful against values computed the same way.
    """
    data = defaultdict(dict)
    backends, tiers, signatures = set(), set(), set()
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                backend = r.get("backend") or "unrecorded"
                index = r["index"]
                data[(backend, index)][r["text"]] = float(r["value"])
            except (TypeError, ValueError, KeyError):
                continue
            if r.get("backend"):
                backends.add(r["backend"])
            if r.get("tier"):
                tiers.add(str(r["tier"]))
            signature_fields = ("backend_version", "python_version", "spacy_version",
                                "spacy_model", "spacy_model_version")
            if all(r.get(field) for field in signature_fields):
                signatures.add("|".join((backend, *(r[field] for field in signature_fields))))
    return data, {"backends": sorted(backends), "tiers": sorted(tiers),
                  "signatures": sorted(signatures)}


def cmd_build(args):
    data, prov = load_tidy(args.metrics)
    if not data:
        sys.exit(f"no usable rows in {args.metrics}")
    texts = {t for vals in data.values() for t in vals}
    n = len(texts)
    if n < MIN_CORPUS:
        print(f"WARNING: corpus has {n} texts. Below ~{MIN_CORPUS} the percentiles are noise "
              f"dressed up as precision -- report them as 'roughly' or not at all.",
              file=sys.stderr)

    norms = {"n_texts": n, "source": args.source or str(args.metrics), "label": args.label,
             "backends": prov["backends"], "tiers": prov["tiers"],
             "signatures": prov["signatures"], "indices": {}}
    for (backend, idx), vals in data.items():
        v = sorted(vals.values())
        if len(v) < 3:
            continue
        norms["indices"][f"{backend}::{idx}"] = {
            "backend": backend, "index": idx,
            "n": len(v), "mean": st.mean(v),
            "sd": st.pstdev(v) if len(v) > 1 else 0.0,
            "values": v,  # kept so percentiles are empirical, not Gaussian-assumed
        }
    Path(args.out).write_text(json.dumps(norms, indent=1), encoding="utf-8")
    print(f"Built norms from {n} texts, {len(norms['indices'])} indices -> {args.out}")
    print(f"Backends: {', '.join(prov['backends']) or 'unrecorded'} "
          f"(tier {'/'.join(prov['tiers']) or '?'})")
    if args.label:
        print(f"Labelled: {args.label}")
    if not prov["backends"]:
        print("NOTE: this metrics file has no backend column, so the provenance check on "
              "compare cannot protect you. Regenerate it with the current run_tools.py.",
              file=sys.stderr)


def percentile_of(value, sorted_values):
    """Empirical percentile: share of corpus at or below this value."""
    below = sum(1 for x in sorted_values if x < value)
    equal = sum(1 for x in sorted_values if x == value)
    return 100.0 * (below + 0.5 * equal) / len(sorted_values)


def check_provenance(norms, prov, force):
    """Refuse to compare values that were not computed the same way.

    The failure this prevents is quiet and total: textdescriptives' embedding-based
    `coherence` and TAACO's lemma-overlap indices measure the same phenomenon on entirely
    different scales. Nothing errors, the percentiles look plausible, and every one of them
    is meaningless. A shared index NAME across backends would make it worse, not better.
    """
    n_backends = set(norms.get("backends") or [])
    d_backends = set(prov["backends"])
    n_signatures = set(norms.get("signatures") or [])
    d_signatures = set(prov.get("signatures") or [])
    if n_signatures and d_signatures and n_signatures != d_signatures:
        msg = ["Runtime provenance mismatch between the draft and the norms.",
               f"  norms: {', '.join(sorted(n_signatures))}",
               f"  draft: {', '.join(sorted(d_signatures))}"]
        if not force:
            msg.append("\nRecompute one side in the same environment, or pass "
                       "--force-provenance only after verifying compatibility.")
            sys.exit("\n".join(msg))
        msg.append("\n--force-provenance given; proceeding. Disclose the mismatch.")
        print("\n".join(msg) + "\n", file=sys.stderr)
        return
    if not n_backends or not d_backends:
        print("WARNING: provenance is unrecorded on one side, so I cannot verify that the "
              "draft and the norms were computed by the same backends. Regenerate both with "
              "the current run_tools.py.\n", file=sys.stderr)
        return
    if n_backends == d_backends:
        return

    only_norms = sorted(n_backends - d_backends)
    only_draft = sorted(d_backends - n_backends)
    msg = ["Backend mismatch between the draft and the norms.",
           f"  norms built with: {', '.join(sorted(n_backends))}",
           f"  draft measured with: {', '.join(sorted(d_backends))}"]
    if only_norms:
        msg.append(f"  in norms only: {', '.join(only_norms)}")
    if only_draft:
        msg.append(f"  in draft only: {', '.join(only_draft)}")

    cross_tier = set(norms.get("tiers") or []) != set(prov["tiers"])
    if cross_tier and not force:
        msg.append("\nThese are different TIERS. Their indices are not commensurable and any "
                   "percentile from this comparison would be fiction. Recompute one side "
                   "with the other's backends.")
        sys.exit("\n".join(msg))
    if not force:
        msg.append("\nSame tier, different backends. Only indices present in both will be "
                   "compared, which may silently narrow the report. Pass --force-provenance "
                   "if you have checked this is what you want.")
        sys.exit("\n".join(msg))
    msg.append("\n--force-provenance given; proceeding. Say in the review that the draft and "
               "the norms were measured with different backends.")
    print("\n".join(msg) + "\n", file=sys.stderr)


def cmd_compare(args):
    norms = json.loads(Path(args.norms).read_text(encoding="utf-8"))
    data, prov = load_tidy(args.metrics)
    check_provenance(norms, prov, args.force_provenance)
    n = norms.get("n_texts", 0)

    rows = []
    for (backend, idx), vals in data.items():
        ref = norms["indices"].get(f"{backend}::{idx}")
        if not ref:
            continue
        layer, gloss = classify(idx)
        if layer is None and not args.all:
            continue
        for text, value in vals.items():
            pct = percentile_of(value, ref["values"])
            z = (value - ref["mean"]) / ref["sd"] if ref["sd"] else 0.0
            rows.append({"text": text, "backend": backend, "index": idx,
                         "layer": layer or "other",
                         "value": value, "pct": pct, "z": z,
                         "mean": ref["mean"], "gloss": gloss or ""})

    if not rows:
        sys.exit("No indices in common between the draft metrics and the norms. Were both "
                 "produced by the same tools and versions?")

    lo, hi = args.low, 100 - args.low
    extreme = [r for r in rows if r["pct"] <= lo or r["pct"] >= hi]
    extreme.sort(key=lambda r: abs(r["pct"] - 50), reverse=True)

    label = norms.get("label") or Path(args.norms).stem
    print("=" * 76)
    print(f"PERCENTILE REPORT against {label} (n={n} texts)")
    print("=" * 76)
    if n < MIN_CORPUS:
        print(f"\n!! Reference corpus is only {n} texts. Treat every number below as a hint, "
              f"\n   not a measurement, and say so when you report it.\n")
    print(f"\n{len(rows)} comparable indices; {len(extreme)} outside the "
          f"{lo:.0f}th-{hi:.0f}th percentile band.\n")

    if not extreme:
        print("Nothing is unusual relative to this corpus. That is a finding: whatever makes\n"
              "this draft hard to read is not visible to these instruments, and the diagnosis\n"
              "belongs at a layer they do not measure.\n")

    by_layer = defaultdict(list)
    for r in extreme:
        by_layer[r["layer"]].append(r)

    for layer in sorted(by_layer):
        print("-" * 76)
        print(f"{layer.upper()}")
        print("-" * 76)
        seen_gloss = set()
        for r in by_layer[layer][: args.top]:
            direction = "LOW " if r["pct"] < 50 else "HIGH"
            print(f"  [{direction} p{r['pct']:4.0f}]  {r['backend']}::{r['index']}")
            print(f"      draft {r['value']:.4g}   corpus mean {r['mean']:.4g}   z={r['z']:+.2f}"
                  + (f"   ({r['text']})"
                     if len(data.get((r['backend'], r['index']), {})) > 1 else ""))
            if r["gloss"] and r["gloss"] not in seen_gloss:
                seen_gloss.add(r["gloss"])
                print(f"      {r['gloss']}")
        if len(by_layer[layer]) > args.top:
            print(f"  (+{len(by_layer[layer]) - args.top} more in this layer)")
        print()

    print("=" * 76)
    print("A percentile is a question, not a verdict. An index sits outside the band for two\n"
          "reasons that look identical here: the draft is doing something readers will\n"
          "struggle with, or the draft is doing something the corpus does not do for reasons\n"
          "of genre, section, or topic. Go read the passage before you report the number.")
    print("=" * 76)

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["text", "backend", "index", "layer",
                                               "value", "pct", "z", "mean", "gloss"])
            w.writeheader()
            w.writerows(sorted(rows, key=lambda r: (r["layer"], r["pct"])))
        print(f"\nFull table -> {args.csv}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build norms from a reference corpus")
    b.add_argument("--metrics", required=True, type=Path, help="tidy CSV from run_tools.py")
    b.add_argument("--out", required=True, type=Path)
    b.add_argument("--label", default="", help='e.g. "Discourse Processes 2019-2024, n=40"')
    b.add_argument("--source", default="",
                   help="human-meaningful corpus source recorded in norms metadata")
    b.set_defaults(func=cmd_build)

    c = sub.add_parser("compare", help="compare a draft against norms")
    c.add_argument("--metrics", required=True, type=Path, help="tidy CSV for the draft")
    c.add_argument("--norms", required=True, type=Path)
    c.add_argument("--low", type=float, default=10.0,
                   help="flag indices below this percentile or above its complement "
                        "(default 10 -> flags p<10 and p>90)")
    c.add_argument("--top", type=int, default=6, help="max indices shown per layer")
    c.add_argument("--all", action="store_true",
                   help="include indices with no mapped diagnostic meaning (noisy)")
    c.add_argument("--force-provenance", action="store_true",
                   help="compare even though the draft and norms used different backends "
                        "(you must then say so when reporting)")
    c.add_argument("--csv", type=Path, default=None, help="also write the full table")
    c.set_defaults(func=cmd_compare)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
