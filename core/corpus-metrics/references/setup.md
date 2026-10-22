# Setup

Two tiers. Start at Tier 1; it is one `pip install` and covers most of what a review needs.
Go to Tier 2 only when the number has to be a *TAACO* number — that is, when you will cite it.

Run `scripts/tcm.py doctor` first. Everything below is context for what it tells you.

## Contents

1. [Tier 1 — pip backends (default)](#tier-1--pip-backends-default)
2. [Tier 2 — the canonical repo tools](#tier-2--the-canonical-repo-tools)
3. [The missing TAACO connective dictionary](#the-missing-taaco-connective-dictionary)
4. [Where this can run](#where-this-can-run)
5. [Not applicable: coh-metrix-dementia](#not-applicable-coh-metrix-dementia)
6. [Building a reference corpus](#building-a-reference-corpus)

---

## Tier 1 — pip backends (default)

```bash
python3.12 -m venv ~/.venvs/textmetrics
source ~/.venvs/textmetrics/bin/activate     # Windows: ~\.venvs\textmetrics\Scripts\activate
pip install -r requirements-tier1.txt
python scripts/tcm.py doctor
```

Use CPython 3.10–3.12. TextDescriptives 2.8.4 requires NumPy `<2`; on Windows, Python 3.13
does not have a compatible NumPy 1.x wheel. The requirements file also pins `setuptools<81`
because TAALED and pylats still import `pkg_resources`, and installs `en_core_web_md` because
the small spaCy model has no static vectors and does not yield trustworthy coherence values.

| Package | Gives you |
|---|---|
| **textdescriptives** | `coherence` (first- and second-order sentence-embedding similarity), `descriptive_stats`, `readability`, `dependency_distance`, `pos_proportions`. The runner omits `quality`: it has no writing-diagnostic mapping here and its 2.8.4 factory is incompatible with current spaCy/Pydantic validation. |
| **taaled** + **pylats** | Lexical diversity, from the same author as desktop TAALED. `pylats` does tokenisation, lemmatisation, homograph disambiguation and misspelling filtering — without it the LD values drift, so install both. |
| **lftk** | ~220 handcrafted features. We pull the `syntax` and `discourse` domains plus surface baselines. |

`textdescriptives` will auto-download a model if you let it. Pin `en_core_web_md` explicitly:
the corpus and draft must use the same parser, and its static vectors are required for the
first- and second-order coherence indices.

## Tier 2 — the canonical repo tools

Use when a value must correspond to published TAACO/TAASSC literature.

```bash
python3.12 -m venv ~/.venvs/tcm-canonical
source ~/.venvs/tcm-canonical/bin/activate
pip install -r requirements-tier1.txt -r requirements-tier2-core.txt
python -m spacy download en_core_web_sm
# The local TAASSC_215_dev.py hardcodes the transformer model; install only if needed:
python -m spacy download en_core_web_trf
python scripts/tcm.py doctor --tools-dir ~/diag-tools
```

Python 3.9–3.11 is the safe range. TAALED's source uses `is ""` comparisons, which are a
`SyntaxWarning` from 3.8 on — noisy, not fatal.

**TAACO.** `runTAACO(indir, outcsv, varDict)` in `TAACOnoGUI.py` — the cleanest entry point of
the four. Resolves data files relative to CWD, so `run_tools.py` chdirs into the TAACO folder
first; do the same if you call it yourself. See the next section about missing files.

**TAASSC.** `LGR_Analysis(text)` for a string, `LGR_Full(folder, outname)` for a directory.
Also CWD-relative — reads `lists_LGR/` from its own folder. Use the highest
`TAASSC_21*_dev.py` present; the published `2.0.0.58` build is a GUI script with no clean API.
Worth keeping in the stack for one reason: the Biber-style phrasal-vs-clausal split, which
nothing in Tier 1 reproduces and which is the interpretive key in `index-map.md` §3.

**TAALED desktop.** Prefer the `taaled` pip package. The desktop version's `main()` was
written to run inside its Tk app — it pushes progress onto a module-global `dataQueue` and
pops modal dialogs on empty input; `run_tools.py` installs inert stand-ins for both. Worse,
it bundles `dep_files/en_core_web_sm` in **spaCy 2.0 format**, which will not load under
spaCy 3.x. `run_tools.py` redirects to the installed model, which works but changes
lemmatisation slightly, so **the values are not comparable to published TAALED norm tables.**
If you need citable TAALED numbers, either use the pip package or make a second venv pinned
to spaCy 2.x.

**ReaderBench.** Heaviest by far — `requirements.txt` pins torch, transformers, gensim,
scikit-learn, nltk and spaCy at specific versions. Give it its own venv.

```bash
python3 -m venv ~/.venvs/readerbench
source ~/.venvs/readerbench/bin/activate
pip install -r ReaderBench/requirements.txt
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

Ignore `usage.py` as a template — it imports Romanian correction modules and Flask and will
fail on both. The path that matters is `Document(Lang.EN, text)` → `CnaGraph(...)` →
`compute_indices(doc)` → `doc.indices`, which is what `run_tools.py` does. The first
`create_vector_model` call downloads a vector model; slow once, cached after.

Worth the trouble only when the question is about **long-range** cohesion — the
cohesion-network graph sees links that adjacent-overlap measures structurally cannot.

## The missing TAACO connective dictionary

`TAACOnoGUI.py` reads `Connectives_DICT_T4.txt`, which is **not present in the upstream
repository** (`github.com/LCR-ADS-Lab/TAACO`). This is not an incomplete clone or a git-lfs
problem. Without it, connective indices cannot compute. `para_files/` is not a dependency;
TAACO creates and cleans that scratch directory itself, so paragraph-overlap indices remain
available.

`run_tools.py` detects their absence and disables the affected options rather than crashing,
but you should say in any review which indices are missing and why.

Three ways to obtain them, best first:

1. **Extract from the compiled desktop build.** `resource_path()` has a `sys._MEIPASS`
   branch, which means TAACO is PyInstaller-packaged and the data files ship *inside* the
   application bundle. Download the build for your platform from
   [linguisticanalysistools.org/taaco.html](https://www.linguisticanalysistools.org/taaco.html)
   and unpack it. This gets the version matched to 2.1.x, so the connective category names
   are guaranteed to line up.
2. **The `schlevik/taaco` fork** ships a `resources.zip` that likely contains the connective
   dictionary. Caveat: that fork is a port of TAACO **2.0.4**, the CoreNLP-era resource set.
   Compare the category names against what 2.1.x expects before trusting the output.
3. **Open an issue** on `LCR-ADS-Lab/TAACO`. This is a genuine packaging bug and the
   maintainers should know.

## Where this can run

**Restricted agent environments may need install approval.** Every backend needs spaCy and a
language model. If the environment cannot persist a venv or reach the package index even with
approval, say plainly that the skill cannot run there; do not substitute a different measure
and present it as equivalent.

**On the author's own machine**, Tier 1 is a two-minute setup and Tier 2 is an afternoon.

## Not applicable: coh-metrix-dementia

If it turns up in the tools directory: it is Coh-Metrix-Port, a **Brazilian Portuguese**
adaptation further specialised for dementia-related speech analysis. It has nothing to
contribute to English academic writing review. Say so rather than trying to make it run.

## Building a reference corpus

The corpus determines whether any of this means anything.

- **Plain text, one file per document.** `run_tools.py` accepts `.md` and strips markup, but
  PDFs must be converted first, and PDF-to-text routinely mangles hyphenation, running heads
  and reference lists. Spot-check two or three converted files by eye. Garbage extraction
  produces confident, wrong percentiles.
- **Strip references, tables, figure captions and author metadata.** Reference lists in
  particular destroy every cohesion measure.
- **Segment by section if you can.** Intro-vs-intros is far more informative than
  whole-article comparison, and it maps onto how the review skills actually work.
- **20 texts is a floor, 40 is comfortable.** `norms.py` warns below 20; pass the warning on
  rather than absorbing it.
- **Use one tier for both sides.** Build the norms and measure the draft with the same
  backends. `norms.py` records provenance and refuses cross-tier comparison, because
  textdescriptives' embedding coherence and TAACO's lemma overlap are on unrelated scales and
  a mixed comparison fails silently rather than loudly.
- **Record what the corpus is** via `norms.py build --label`. The label prints in every
  report, which stops a percentile drifting loose from the population that defines it.
