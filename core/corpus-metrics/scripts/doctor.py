#!/usr/bin/env python3
"""
doctor.py -- report which backends can actually run here, and pick a tier.

Run this FIRST, every time, before promising anyone any numbers. Tier-2 tools in particular
fail silently and confusingly; knowing what is broken beforehand is worth thirty seconds.

    python scripts/tcm.py doctor                          # tier 1 only
    python scripts/tcm.py doctor --tools-dir ~/diag-tools # also check tier 2

Exit 0 if at least one backend is runnable, 1 otherwise.
"""

import argparse
import importlib.metadata
import importlib.util
import json
import sys
from pathlib import Path

OK, WARN, BAD = "OK  ", "WARN", "FAIL"


def have(mod):
    try:
        return importlib.util.find_spec(mod) is not None
    except (ImportError, ValueError):
        return False


def version_of(mod):
    try:
        return importlib.metadata.version(mod)
    except importlib.metadata.PackageNotFoundError:
        return None


def find_one(root, *patterns):
    for p in patterns:
        hits = sorted(root.glob(p))
        if hits:
            return hits[0]
    return None


def check_env(spacy_model):
    rows, spacy_major, spacy_ok = [], 0, False
    rows.append((OK, "python", f"{sys.version_info.major}.{sys.version_info.minor}"
                               f".{sys.version_info.micro}"))
    v = version_of("spacy") if have("spacy") else None
    if v:
        rows.append((OK, "spacy", v))
        spacy_major = int(str(v).split(".")[0]) if str(v)[0].isdigit() else 0
        try:
            import spacy
            nlp = spacy.load(spacy_model)
            if nlp.vocab.vectors_length:
                rows.append((OK, spacy_model,
                             f"loadable; {nlp.vocab.vectors_length}-dimensional vectors"))
            else:
                rows.append((WARN, spacy_model, "loadable, but has no static word vectors; "
                             "TextDescriptives coherence will not be reliable. Install "
                             "en_core_web_md or en_core_web_lg."))
            spacy_ok = True
        except Exception as e:
            rows.append((BAD, spacy_model, f"not loadable ({type(e).__name__}) -- "
                                           f"python -m spacy download {spacy_model}"))
    else:
        rows.append((BAD, "spacy", "not installed -- pip install spacy"))
    return rows, spacy_major, spacy_ok


def check_tier1(spacy_ok):
    """Everything here is a pip install away. No repo, no version surgery."""
    out = {}
    gate = None if spacy_ok else "spaCy model unavailable, so this cannot run"

    if not have("textdescriptives"):
        out["textdescriptives"] = (BAD, "pip install textdescriptives", None)
    elif gate:
        out["textdescriptives"] = (BAD, gate, version_of("textdescriptives"))
    else:
        out["textdescriptives"] = (OK, "coherence, descriptive_stats, readability, "
                                       "dependency_distance, pos_proportions",
                                   version_of("textdescriptives"))

    if not have("taaled"):
        out["taaled"] = (BAD, "pip install taaled pylats", None)
    elif not have("pylats"):
        out["taaled"] = (WARN, "installed, but pylats absent -- without it there is no "
                               "homograph disambiguation or misspelling filter and values "
                               "drift. pip install pylats", version_of("taaled"))
    elif gate:
        out["taaled"] = (BAD, gate, version_of("taaled"))
    else:
        out["taaled"] = (OK, "lexical diversity, official pip package (see index-map.md "
                             "§4 on what these numbers do and do not license)",
                         version_of("taaled"))

    if not have("lftk"):
        out["lftk"] = (BAD, "pip install lftk", None)
    elif gate:
        out["lftk"] = (BAD, gate, version_of("lftk"))
    else:
        out["lftk"] = (OK, "~220 handcrafted features; syntax + discourse domains used",
                       version_of("lftk"))
    return out


def check_tier2(tools_dir: Path, spacy_major: int, spacy_ok: bool):
    """The canonical instruments. Every one parses with spaCy, so a missing model makes them
    all unrunnable no matter how healthy their own files look."""
    out = {}
    gate = None if spacy_ok else "spaCy model unavailable, so this cannot run"

    # ---- TAACO
    t = tools_dir / "TAACO"
    entry = find_one(t, "TAACOnoGUI.py")
    if entry is None:
        out["taaco"] = (BAD, "TAACOnoGUI.py not found", None)
    elif not have("en_core_web_sm"):
        out["taaco"] = (BAD, "TAACO hardcodes en_core_web_sm; install that model", str(t))
    else:
        missing = [d for d in ("Connectives_DICT_T4.txt", "wn_noun_2.txt", "wn_verb_2.txt")
                   if not (t / d).exists()]
        if gate:
            out["taaco"] = (BAD, gate, str(t))
        elif missing:
            out["taaco"] = (WARN,
                            f"runnable, but missing {', '.join(missing)}. These are absent "
                            f"from the upstream repo itself, not from your clone -- see "
                            f"references/setup.md for the three ways to obtain them. "
                            f"run_tools.py disables the affected indices automatically.",
                            str(t))
        else:
            note = "runTAACO(indir, outcsv, varDict)"
            if spacy_major and spacy_major < 3:
                note += "  [spaCy 2 detected; TAACO 2.1.x targets spaCy 3]"
            out["taaco"] = (OK, note, str(t))

    # ---- TAASSC
    entry = find_one(tools_dir / "TAASSC", "**/TAASSC_215_dev.py",
                     "**/TAASSC_214_dev.py", "**/TAASSC_213_dev.py")
    if entry is None:
        out["taassc"] = (BAD, "no TAASSC_21*_dev.py found", None)
    elif not (entry.parent / "lists_LGR").is_dir():
        out["taassc"] = (BAD, "lists_LGR/ not found next to the module", str(entry.parent))
    elif not have("lexical_diversity"):
        out["taassc"] = (BAD, "missing lexical-diversity -- install "
                               "requirements-tier2-core.txt", str(entry.parent))
    elif "en_core_web_trf" in entry.read_text(encoding="utf-8", errors="ignore") and not have("en_core_web_trf"):
        out["taassc"] = (BAD, f"{entry.name} hardcodes en_core_web_trf; install the model "
                               "and its transformer dependencies", str(entry.parent))
    elif gate:
        out["taassc"] = (BAD, gate, str(entry.parent))
    else:
        out["taassc"] = (OK, f"LGR_Full() in {entry.name}; the Biber phrasal/clausal split "
                             f"is what makes this worth keeping", str(entry.parent))

    # ---- TAALED desktop
    entry = find_one(tools_dir / "TAALED", "**/TAALED_1_4_1.py", "**/TAALED_1_3_1.py")
    if entry is None:
        out["taaled_desktop"] = (BAD, "no TAALED_1_*.py found", None)
    elif not have("en_core_web_sm"):
        out["taaled_desktop"] = (BAD, "desktop redirect requires en_core_web_sm", str(entry.parent))
    elif gate:
        out["taaled_desktop"] = (BAD, gate, str(entry.parent))
    else:
        note = "GUI-coupled main(); run_tools.py stubs dataQueue and tkinter"
        status = OK
        meta = entry.parent / "dep_files" / "en_core_web_sm" / "meta.json"
        if meta.exists() and spacy_major >= 3:
            try:
                bundled = json.loads(meta.read_text()).get("spacy_version", "?")
            except Exception:
                bundled = "?"
            status = WARN
            note = (f"bundled model is spaCy {bundled} format, unloadable under "
                    f"spaCy {spacy_major}.x; run_tools.py redirects to the installed model, "
                    f"so values are not comparable to published TAALED norm tables. "
                    f"Prefer the `taaled` pip package unless you specifically need desktop "
                    f"-comparable values. " + note)
        out["taaled_desktop"] = (status, note, str(entry.parent))

    # ---- ReaderBench
    t = tools_dir / "ReaderBench"
    if not (t / "rb").is_dir():
        out["readerbench"] = (BAD, "rb/ package not found", None)
    else:
        missing = [m for m in ("torch", "transformers", "nltk", "gensim", "sklearn", "spacy")
                   if not have(m)]
        out["readerbench"] = ((BAD, f"missing heavy dependencies: {', '.join(missing)}", str(t))
                              if missing else
                              (OK, "cohesion-network graph; the only backend that sees "
                                   "long-range links", str(t)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tools-dir", type=Path, default=None,
                    help="directory holding TAACO/, TAASSC/, ... (omit to check tier 1 only)")
    ap.add_argument("--spacy-model", default="en_core_web_md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    env_rows, spacy_major, spacy_ok = check_env(args.spacy_model)
    tier1 = check_tier1(spacy_ok)
    tier2 = {}
    if args.tools_dir:
        td = args.tools_dir.expanduser().resolve()
        if not td.is_dir():
            sys.exit(f"tools dir not found: {td}")
        tier2 = check_tier2(td, spacy_major, spacy_ok)

    ready1 = [k for k, v in tier1.items() if v[0] in (OK, WARN)]
    ready2 = [k for k, v in tier2.items() if v[0] in (OK, WARN)]
    recommended = 1 if ready1 else (2 if ready2 else None)

    if args.json:
        print(json.dumps({
            "env": [{"status": s.strip(), "item": i, "detail": d} for s, i, d in env_rows],
            "tier1": {k: {"status": v[0].strip(), "detail": v[1], "version_or_path": v[2]}
                      for k, v in tier1.items()},
            "tier2": {k: {"status": v[0].strip(), "detail": v[1], "version_or_path": v[2]}
                      for k, v in tier2.items()},
            "runnable": {"tier1": ready1, "tier2": ready2},
            "recommended_tier": recommended,
        }, indent=2))
    else:
        print("=" * 72)
        print("ENVIRONMENT")
        print("=" * 72)
        for s, i, d in env_rows:
            print(f"  [{s}] {i:<18} {d}")

        for label, group in (("TIER 1 -- pip backends (default)", tier1),
                             ("TIER 2 -- canonical repo tools (citable)", tier2)):
            if not group:
                continue
            print("\n" + "=" * 72)
            print(label)
            print("=" * 72)
            for name, (s, detail, extra) in group.items():
                print(f"  [{s}] {name}" + (f"  ({extra})" if extra and len(extra) < 20 else ""))
                print(f"         {detail}")
                if extra and len(extra) >= 20:
                    print(f"         at {extra}")
        if not tier2:
            print("\n(Tier 2 not checked -- pass --tools-dir to include it.)")

        print()
        if recommended == 1:
            print(f"Use tier 1: {', '.join(ready1)}")
            print("  python scripts/tcm.py measure --input <draft-or-corpus> "
                  "--tier 1 --out metrics.csv")
        elif recommended == 2:
            print(f"Tier 1 unavailable. Use tier 2: {', '.join(ready2)}")
            print("  python scripts/tcm.py measure --input <x> --tier 2 "
                  "--tools-dir <dir> --out metrics.csv")
        else:
            print("Nothing is runnable. Say so, and do not substitute a different "
                  "measurement and present it as equivalent.")
        if ready1 and ready2:
            print("\nBoth tiers available. Tier 1 unless the number will be cited -- and "
                  "never build norms in one tier and compare a draft in the other.")

    sys.exit(0 if recommended else 1)


if __name__ == "__main__":
    main()
