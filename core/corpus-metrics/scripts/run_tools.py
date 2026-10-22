#!/usr/bin/env python3
"""
run_tools.py -- compute text indices with whichever backend is available, emit tidy output.

TWO TIERS, and the difference matters more than it looks:

  Tier 1 (pip):   textdescriptives, taaled, lftk
                  One `pip install` away. Maintained, importable, no version hacks.
                  DEFAULT.

  Tier 2 (repos): TAACO, TAASSC, TAALED-desktop, ReaderBench
                  The canonical instruments from the published literature. Use when the
                  number has to BE a TAACO number -- i.e. when you will cite it.

The two tiers do not produce the same indices. textdescriptives' `coherence` is
embedding-based first/second-order similarity between sentences; TAACO's
`adjacent_overlap_content_sent` is lemma-type overlap. They point at the same phenomenon and
are numerically unrelated. Percentiles built within one tier are meaningful; percentiles
compared across tiers are not, which is why every row carries its backend and tier and why
norms.py refuses to mix them.

    python3 run_tools.py --input draft.md --tier 1
    python3 run_tools.py --input corpus/ --tier 1 --out corpus_tidy.csv
    python3 run_tools.py --input draft.md --tier 2 --tools-dir ~/diag-tools --backend taaco,taassc

Output: text,backend,tier,index,value
"""

import argparse
import contextlib
import csv
import io
import importlib.metadata
import os
import shutil
import sys
import tempfile
import types
import warnings
from pathlib import Path

TIER1 = ["textdescriptives", "taaled", "lftk"]
TIER2 = ["taaco", "taassc", "taaled_desktop", "readerbench"]


def package_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "source-tree"


def effective_spacy_model(backend, requested):
    """Return the model a backend actually loads, not merely the CLI default."""
    return {"taaco": "en_core_web_sm",
            "taassc": "en_core_web_trf",
            "taaled_desktop": "en_core_web_sm",
            "readerbench": "readerbench-managed"}.get(backend, requested)


# --------------------------------------------------------------------------- helpers

@contextlib.contextmanager
def pushd(path):
    """Tier-2 tools resolve their data files relative to CWD, so we must chdir."""
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


@contextlib.contextmanager
def syspath(path):
    p = str(path)
    sys.path.insert(0, p)
    try:
        yield
    finally:
        with contextlib.suppress(ValueError):
            sys.path.remove(p)


def strip_markdown(text):
    """These tools expect prose. Headings, fences and bullets otherwise become sentences
    and distort every cohesion index -- silent corruption that makes a percentile a lie."""
    import re
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    out = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("#") or s.startswith("|") or set(s) <= set("-=|* "):
            continue
        s = re.sub(r"^[-*+]\s+", "", s)
        s = re.sub(r"^\d+\.\s+", "", s)
        s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"\*\*|__|\*|_", "", s)
        out.append(s)
    return "\n".join(out)


def stage_inputs(input_path: Path, workdir: Path) -> Path:
    """Tier-2 tools take a directory of .txt files; Tier-1 reads the same staged files."""
    indir = workdir / "input"
    indir.mkdir(parents=True, exist_ok=True)
    files = [input_path] if input_path.is_file() else sorted(
        p for p in input_path.rglob("*") if p.suffix.lower() in {".txt", ".md"})
    if not files:
        sys.exit(f"No .txt or .md files found under {input_path}")
    by_stem = {}
    for f in files:
        by_stem.setdefault(f.stem.casefold(), []).append(f)
    collisions = [group for group in by_stem.values() if len(group) > 1]
    if collisions:
        detail = "; ".join(", ".join(str(p) for p in group) for group in collisions)
        sys.exit("Input filenames must have unique stems because downstream tools identify "
                 f"documents by filename. Rename these collisions: {detail}")
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        if f.suffix.lower() == ".md":
            text = strip_markdown(text)
        if not text.strip():
            sys.exit(f"Input contains no prose after preprocessing: {f}")
        (indir / (f.stem + ".txt")).write_text(text, encoding="utf-8")
    return indir


def flatten(prefix, obj, rows, text, backend, tier):
    """Index values arrive as nested dicts from several backends. Flatten to leaves."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            flatten(f"{prefix}_{k}" if prefix else str(k), v, rows, text, backend, tier)
        return
    try:
        val = float(obj)
    except (TypeError, ValueError):
        return
    if val != val:  # NaN
        return
    rows.append({"text": text, "backend": backend, "tier": tier,
                 "index": prefix, "value": val})


def read_wide_csv(path: Path, backend: str, tier: int):
    rows = []
    if not path.exists():
        return rows
    with open(path, newline="", encoding="utf-8", errors="ignore") as fh:
        rdr = csv.DictReader(fh)
        namecol = next((c for c in (rdr.fieldnames or [])
                        if c and c.lower() in ("filename", "file", "text", "name", "id")), None)
        for r in rdr:
            text = Path(r.get(namecol, "?") if namecol else "?").stem
            for k, v in r.items():
                if k == namecol or k is None:
                    continue
                try:
                    rows.append({"text": text, "backend": backend, "tier": tier,
                                 "index": k, "value": float(v)})
                except (TypeError, ValueError):
                    continue
    return rows


# --------------------------------------------------------------- TIER 1 (pip backends)

def run_textdescriptives(indir: Path, spacy_model: str, **_):
    """Cohesion/coherence, descriptive stats, readability, dependency distance, POS
    proportions. The `coherence` component is the closest pip-installable analogue to
    TAACO's adjacent-overlap family -- closest, not equivalent."""
    import textdescriptives as td
    rows = []
    # `quality` is intentionally excluded. It is not used by the writing-diagnostic map,
    # and TextDescriptives 2.8.4's quality factory is incompatible with newer spaCy/Pydantic
    # validation (its list defaults are rejected for tuple-typed settings). Keeping it here
    # made the useful cohesion and density metrics fail as collateral damage.
    metrics = ["descriptive_stats", "readability", "dependency_distance",
               "pos_proportions", "coherence"]
    for f in sorted(indir.glob("*.txt")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        df = td.extract_metrics(text=text, spacy_model=spacy_model, metrics=metrics)
        for col in df.columns:
            if col == "text":
                continue
            flatten(str(col), df.iloc[0][col], rows, f.stem, "textdescriptives", 1)
    return rows


def run_taaled(indir: Path, spacy_model: str, **_):
    """Kyle's own pip package. Replaces the GUI-coupled desktop TAALED entirely, and with
    it the spaCy-2-model conflict. Read index-map.md §4 before letting these numbers shape
    any writing advice -- lexical diversity measures proficiency, not reader value."""
    # Both packages print optional-plotting notices at import time. Keep the runner's output
    # reserved for actionable diagnostics.
    with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API.*")
        from taaled import ld
        try:
            from pylats import lats
            have_pylats = True
        except ImportError:
            have_pylats = False

    if have_pylats:
        # pylats 0.64 uses two distinct parameter classes: one to preprocess with spaCy,
        # then one to normalize/lemmatize. Older examples on the web collapse these steps.
        lats.EnSm.model = spacy_model
        with contextlib.redirect_stdout(io.StringIO()):
            lats.load_model(lats.EnSm)

    rows = []
    for f in sorted(indir.glob("*.txt")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        if have_pylats:
            preprocessed = lats.preProcess(text, lats.EnSm)
            toks = lats.Normalize(preprocessed, lats.EnDefault).toks
        else:
            # Untagged fallback. TAALED's homograph disambiguation and misspelling filter
            # are pylats's job; without them values drift, so say so rather than pretend.
            print("  [taaled] pylats absent -- using naive tokenisation; values will differ "
                  "from properly preprocessed ones")
            toks = [w.lower() for w in text.split() if w.strip(".,;:!?()[]\"'")]
        if len(toks) < 50:
            print(f"  [taaled] {f.stem}: {len(toks)} tokens, below the ~50-token floor "
                  f"several LD indices assume. Skipping.")
            continue
        vals = ld.lexdiv(toks)
        # `.vald` is the package's public scalar summary. Walking every object attribute
        # also emits token-frequency dictionaries and per-window diagnostics, bloating each
        # document from 13 interpretable indices to hundreds of accidental rows.
        flatten("", vals.vald, rows, f.stem, "taaled", 1)
    return rows


def run_lftk(indir: Path, spacy_model: str, **_):
    """~220 handcrafted features. We take the syntax and discourse domains (which bear on
    the sentence-density and cohesion questions) plus surface baselines, and skip the rest."""
    import spacy
    import lftk
    nlp = spacy.load(spacy_model)

    keys = []
    for domain in ("syntax", "discourse", "surface"):
        with contextlib.suppress(Exception):
            keys += lftk.search_features(domain=domain, return_format="list_key") or []
    for family in ("partofspeech", "avgpartofspeech", "typetokenratio", "lexicalvariation"):
        with contextlib.suppress(Exception):
            keys += lftk.search_features(family=family, return_format="list_key") or []
    keys = sorted(set(keys))
    if not keys:
        raise RuntimeError("lftk.search_features returned nothing; API may have changed")

    rows = []
    for f in sorted(indir.glob("*.txt")):
        doc = nlp(f.read_text(encoding="utf-8", errors="ignore"))
        ex = lftk.Extractor(docs=doc)
        ex.customize(stop_words=True, punctuations=False, round_decimal=4)
        flatten("", ex.extract(features=keys), rows, f.stem, "lftk", 1)
    return rows


# ------------------------------------------------------------ TIER 2 (repo backends)

def run_taaco(indir: Path, tools_dir: Path, workdir: Path, **_):
    root = tools_dir / "TAACO"
    if not (root / "TAACOnoGUI.py").exists():
        raise RuntimeError("TAACOnoGUI.py not found")
    # Connective indices need a dictionary missing from the upstream repo. `para_files/`, by
    # contrast, is TAACO's generated scratch directory; its absence must not disable paragraph
    # overlap (TAACO creates and cleans it itself).
    has_conn = (root / "Connectives_DICT_T4.txt").exists()
    if not has_conn:
        print("  [taaco] Connectives_DICT_T4.txt absent -- connective indices disabled")

    variables = {
        "sourceKeyOverlap": False, "sourceLSA": False, "sourceLDA": False,
        "sourceWord2vec": False,
        "wordsAll": True, "wordsContent": True, "wordsFunction": True, "wordsNoun": True,
        "wordsPronoun": True, "wordsArgument": True, "wordsVerb": True,
        "wordsAdjective": True, "wordsAdverb": True,
        "overlapSentence": True, "overlapParagraph": True, "overlapAdjacent": True,
        "overlapAdjacent2": True,
        "otherTTR": True, "otherConnectives": has_conn, "otherGivenness": True,
        "overlapLSA": True, "overlapLDA": True, "overlapWord2vec": True,
        "overlapSynonym": True, "overlapNgrams": True,
        "outputTagged": False, "outputDiagnostic": False,
    }
    out = (workdir / "taaco_wide.csv").resolve()
    with syspath(root), pushd(root):
        from TAACOnoGUI import runTAACO
        runTAACO(str(indir.resolve()) + os.sep, str(out), variables)
    return read_wide_csv(out, "taaco", 2)


def run_taassc(indir: Path, tools_dir: Path, workdir: Path, **_):
    cands = sorted((tools_dir / "TAASSC").rglob("TAASSC_21*_dev.py"), reverse=True)
    if not cands:
        raise RuntimeError("no TAASSC_21*_dev.py found")
    entry = cands[0]
    out = (workdir / "taassc_wide.csv").resolve()
    with syspath(entry.parent), pushd(entry.parent):
        mod = __import__(entry.stem)
        mod.LGR_Full(str(indir.resolve()) + os.sep, str(out))
    return read_wide_csv(out, "taassc", 2)


def run_taaled_desktop(indir: Path, tools_dir: Path, workdir: Path, **_):
    """Only worth using if you need values comparable to the desktop build. Otherwise the
    `taaled` pip package is strictly better -- no GUI globals, no model-format conflict."""
    cands = sorted((tools_dir / "TAALED").rglob("TAALED_1_*.py"), reverse=True)
    if not cands:
        raise RuntimeError("no TAALED_1_*.py found")
    entry = cands[0]

    class _Q:
        def put(self, *a, **k):
            if a:
                print(f"  [taaled_desktop] {a[0]}")

    fake_tk = types.ModuleType("tkinter")
    fake_box = types.ModuleType("tkinter.messagebox")
    fake_box.showinfo = lambda *a, **k: None
    fake_tk.messagebox = fake_box
    saved = {k: sys.modules.get(k) for k in ("tkinter", "tkinter.messagebox")}
    sys.modules["tkinter"], sys.modules["tkinter.messagebox"] = fake_tk, fake_box

    out = (workdir / "taaled_desktop_wide.csv").resolve()
    var_dict = {"indout": False, "aw": True, "cw": True, "fw": True,
                "simple_ttr": True, "root_ttr": True, "log_ttr": True, "maas_ttr": True,
                "mattr": True, "msttr": True, "hdd": True, "mtld_wrap": True,
                "mltd": True, "mltd_ma": True}
    try:
        with syspath(entry.parent), pushd(entry.parent):
            mod = __import__(entry.stem)
            mod.dataQueue = _Q()
            try:
                import spacy
                if int(spacy.__version__.split(".")[0]) >= 3:
                    orig = mod.resource_path
                    mod.resource_path = lambda rel: ("en_core_web_sm"
                                                     if "en_core_web_sm" in rel else orig(rel))
            except Exception:
                pass
            mod.main(str(indir.resolve()) + os.sep, str(out), var_dict)
    finally:
        for k, v in saved.items():
            sys.modules[k] = v if v is not None else sys.modules.pop(k, None)
    return read_wide_csv(out, "taaled_desktop", 2)


def run_readerbench(indir: Path, tools_dir: Path, **_):
    """Worth its heavy setup only for the cohesion-network graph, which sees long-range
    links that adjacent-overlap measures structurally cannot."""
    root = tools_dir / "ReaderBench"
    if not (root / "rb").is_dir():
        raise RuntimeError("ReaderBench rb/ package not found")
    rows = []
    with syspath(root):
        from rb.core.lang import Lang
        from rb.core.document import Document
        from rb.complexity.complexity_index import compute_indices
        from rb.similarity.vector_model_factory import create_vector_model
        from rb.similarity.vector_model import VectorModelType, CorporaEnum
        from rb.cna.cna_graph import CnaGraph

        model = create_vector_model(Lang.EN, VectorModelType.WORD2VEC, CorporaEnum.COCA.value)
        for f in sorted(indir.glob("*.txt")):
            doc = Document(Lang.EN, f.read_text(encoding="utf-8", errors="ignore"))
            CnaGraph(docs=[doc], models=[model])
            compute_indices(doc=doc)
            for idx, val in doc.indices.items():
                flatten(str(idx), val, rows, f.stem, "readerbench", 2)
    return rows


BACKENDS = {
    "textdescriptives": (run_textdescriptives, 1),
    "taaled": (run_taaled, 1),
    "lftk": (run_lftk, 1),
    "taaco": (run_taaco, 2),
    "taassc": (run_taassc, 2),
    "taaled_desktop": (run_taaled_desktop, 2),
    "readerbench": (run_readerbench, 2),
}


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, type=Path,
                    help="a single draft, or a directory of reference texts")
    ap.add_argument("--tier", type=int, choices=[1, 2], default=1,
                    help="1 = pip backends (default), 2 = the canonical repo tools")
    ap.add_argument("--backend", default=None,
                    help="comma-separated subset; defaults to all backends in the tier")
    ap.add_argument("--tools-dir", type=Path, default=None,
                    help="required for tier 2: directory holding TAACO/, TAASSC/, ...")
    ap.add_argument("--spacy-model", default="en_core_web_md",
                    help="spaCy English model; the default includes static vectors needed "
                         "for meaningful TextDescriptives coherence")
    ap.add_argument("--out", type=Path, default=Path("metrics_tidy.csv"))
    ap.add_argument("--workdir", type=Path, default=None)
    args = ap.parse_args()

    chosen = ([b.strip() for b in args.backend.split(",") if b.strip()]
              if args.backend else (TIER1 if args.tier == 1 else TIER2))
    unknown = [b for b in chosen if b not in BACKENDS]
    if unknown:
        sys.exit(f"unknown backend(s): {', '.join(unknown)}. Known: {', '.join(BACKENDS)}")

    tiers = {BACKENDS[b][1] for b in chosen}
    if len(tiers) > 1:
        sys.exit("Refusing to mix tier 1 and tier 2 backends in one run. Their indices are "
                 "not commensurable, and a CSV containing both invites a percentile "
                 "comparison that means nothing. Run them separately.")

    if 2 in tiers and not args.tools_dir:
        sys.exit("--tools-dir is required for tier 2 backends")

    tmp = None
    if args.workdir:
        workdir = args.workdir.expanduser().resolve()
        workdir.mkdir(parents=True, exist_ok=True)
    else:
        tmp = tempfile.mkdtemp(prefix="tcm_")
        workdir = Path(tmp)

    try:
        indir = stage_inputs(args.input.expanduser().resolve(), workdir)
        n = len(list(indir.glob("*.txt")))
        print(f"Staged {n} text(s). Tier {args.tier}: {', '.join(chosen)}")

        rows, failed = [], {}
        for b in chosen:
            fn, tier = BACKENDS[b]
            print(f"\nRunning {b} ...")
            try:
                got = fn(indir=indir,
                         tools_dir=args.tools_dir.expanduser().resolve() if args.tools_dir
                         else None,
                         workdir=workdir, spacy_model=args.spacy_model)
                backend_version = package_version(b) if tier == 1 else "source-tree"
                try:
                    spacy_version = importlib.metadata.version("spacy")
                except importlib.metadata.PackageNotFoundError:
                    spacy_version = "unavailable"
                model_name = effective_spacy_model(b, args.spacy_model)
                try:
                    model_version = importlib.metadata.version(model_name.replace("_", "-"))
                except importlib.metadata.PackageNotFoundError:
                    model_version = "unrecorded"
                for row in got:
                    row.update({"schema_version": 2,
                                "python_version": ".".join(map(str, sys.version_info[:3])),
                                "backend_version": backend_version,
                                "spacy_version": spacy_version,
                                "spacy_model": model_name,
                                "spacy_model_version": model_version})
                rows.extend(got)
                print(f"  {b}: {len(got)} index values across {n} text(s)")
            except Exception as e:
                failed[b] = f"{type(e).__name__}: {e}"
                print(f"  {b} FAILED -- {failed[b]}")

        if rows:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with open(args.out, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(
                    fh,
                    fieldnames=["schema_version", "text", "backend", "backend_version",
                                "tier", "python_version", "spacy_version", "spacy_model",
                                "spacy_model_version", "index", "value"],
                )
                w.writeheader()
                w.writerows(rows)
            print(f"\nWrote {len(rows)} rows to {args.out}")
        else:
            print("\nNo indices produced.")

        if failed:
            print("\nFailures. Report these to the user; do not quietly substitute another "
                  "backend's numbers, because they are not the same numbers:")
            for b, msg in failed.items():
                print(f"  {b}: {msg}")
        sys.exit(0 if rows else 1)
    finally:
        if tmp and not args.workdir:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
