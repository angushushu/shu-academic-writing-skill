---
name: corpus-metrics
description: >-
  OPTIONAL MODULE, heavy dependencies. Compute cohesion, syntactic-density and lexical
  indices for a draft and express them as percentiles against a reference corpus of the
  author's target venue. This is an instrument, not a review — it produces norm-referenced
  evidence for `core/engineer-argument/` and `core/polish-prose/` to interpret, and it does
  not write feedback on its own. Use when a review needs to say whether a cohesion,
  complexity or lexical measure is actually unusual for the field rather than merely
  reporting a raw number; when the author asks how their prose compares to published work in
  their venue; or when someone wants to build norms from a corpus of articles. Requires
  spaCy — run `python scripts/tcm.py doctor` first and report honestly if the environment
  cannot support it.
---

> **Where this module sits.** Part of the stage model in `SKILL.md`, mapped in
> `core/MODULE-MAP.md`. Before declaring any draft submission-ready, read
> `core/audit-manuscript/SKILL.md` — the adversarial gate every other module stops short of.

# Corpus Metrics (optional)

This module exists to do one thing the review modules cannot do alone: **say whether a number
is unusual.** A review reporting "nominalization density 72.5 per thousand words" has told
the author nothing, because neither of you knows what 72.5 means for *Discourse Processes*. A
review reporting "your adjacent-sentence coherence sits at the 12th percentile against 40
articles from your target venue" has given them evidence.

## What this module is not

It is not a third layer of diagnosis and it does not produce a review. Every index here is a
property **intrinsic to the text** — and the framework the review modules apply rests on the
opposite claim, that value exists only relative to a reader community. No automated index
reaches the value, problem, or code layers. They reach the sentence layer and part of the
movement layer, and that is the honest boundary of their usefulness.

So `core/engineer-argument/` and `core/polish-prose/` call this module when corpus norms are available
and would sharpen a claim they are already making. Neither depends on it. If you find
yourself leading a review with percentile tables, you have inverted the relationship — the
numbers corroborate a reading, never substitute for one.

## Two tiers, and why the difference is load-bearing

| | Backends | When |
|---|---|---|
| **Tier 1** (default) | `textdescriptives`, `taaled`, `lftk` | One `pip install`. Maintained, importable, no version surgery. Use this unless told otherwise. |
| **Tier 2** | TAACO, TAASSC, TAALED-desktop, ReaderBench | The canonical instruments from the published literature. Use when the number has to *be* a TAACO number — i.e. when the author will cite it. |

**The two tiers do not produce the same indices.** textdescriptives' `coherence` is
embedding-based similarity between sentences; TAACO's `adjacent_overlap_content_sent` is
lemma-type overlap. They point at the same phenomenon on unrelated scales. Percentiles built
within one tier are meaningful; percentiles compared across tiers are fiction that looks
plausible. `run_tools.py` refuses to mix tiers in a run and `norms.py` refuses to compare
across them — do not reach for `--force-provenance` to get past this without understanding
why it fired.

Tier 1 covers most of what a writing review needs. Two things it cannot do: connective
incidence *by semantic category* (TAACO) and the phrasal-vs-clausal complexity split
(TAASSC). If the finding is "this accumulates rather than argues" or "this density is
phrasal, not clausal," that needs Tier 2.

## Before anything else, check the environment

```bash
python scripts/tcm.py doctor                          # tier 1
python scripts/tcm.py doctor --tools-dir <diag-tools> # also check tier 2
```

`doctor.py` reports which backends are runnable, recommends a tier, and names the exact fix
for each failure. **If nothing can run, say so and stop — do not substitute the
`textmetrics.py` output from the review modules and present it as if it were this.** An author
who thinks they have norm-referenced data when they have un-normed counts will make worse
decisions than one who knows they have nothing.

The launcher discovers a project-local `.venv` without activation; set `TCM_PYTHON` to an
exact interpreter when the environment lives elsewhere. Read `references/setup.md` for
installation, compatibility constraints, known breakages, and the routes to TAACO's missing
connective dictionary.

## Contract for calling this module

Use `scripts/tcm.py` as the stable entry point. Do not call backend modules directly from
another module. Resolve this module's folder relative to the bundle root (`core/corpus-metrics/`), then
run the launcher with any Python that has stdlib; it will locate the nearest `.venv`.

- Check readiness: `python <bundle-root>/core/corpus-metrics/scripts/tcm.py doctor --json`
- Build norms in one call: `python <bundle-root>/core/corpus-metrics/scripts/tcm.py build --input <corpus-dir> --out <norms.json> --label <corpus-description>`
- Evaluate a draft in one call: `python <bundle-root>/core/corpus-metrics/scripts/tcm.py compare --input <draft> --norms <norms.json>`

Treat a nonzero exit as no result. The tidy metrics record backend, backend version, spaCy
version, and model; `norms.py` refuses a comparison when those do not match. Never strip these
fields or merge same-named indices across backends.

## Workflow

### 1. Build norms — this step is the analysis

```bash
python scripts/tcm.py build --input <corpus-dir>/ --out norms.json \
    --label "Discourse Processes 2019-2024, intros only, n=40"
```

The corpus is the author's to assemble and its composition *is* the finding. Norms from 40
articles in their exact target venue mean something; norms from assorted PDFs produce
percentiles that look authoritative and are not.

Three things to insist on, because these are how it goes wrong quietly:

- **Match the venue, not the field.** "Cognitive psychology" is not a venue. Reviewer
  expectations are journal-specific, which is the whole premise of the code layer.
- **Match the section.** A methods section compared against whole articles looks anomalous on
  every cohesion index for reasons unrelated to quality. Compare intros to intros.
- **Below ~20 texts, report percentiles as impressions.** `norms.py` warns; pass the warning
  on rather than absorbing it.

### 2. Run the draft and compare

```bash
python scripts/tcm.py compare --input draft.md --norms norms.json
```

`compare` reports only indices outside the 10th–90th percentile band, grouped by the
diagnostic layer they bear on, each with a gloss on what the index actually measures.
Everything inside the band is suppressed deliberately: a table of 300 unremarkable numbers
buries the four that matter.

**When nothing is flagged, that is a result worth reporting.** It means whatever makes the
draft hard to read is invisible to these instruments — which usually means the problem lives
at the value or problem layer, exactly where `core/engineer-argument/` works.

### 3. Hand the numbers back as evidence, not as findings

A percentile earns its place in a review only when attached to a passage the reader can see.
The useful shape is *reading first, number second*:

> Your paragraphs 1–6 kept sending me back to re-read. The instrument agrees and says where:
> first-order coherence is at the 8th percentile against your venue while second-order sits
> near the median — which means two threads alternating rather than one developing.
> Concretely, paragraph 2 opens on "problem state" and "goal state," two terms that appear
> nowhere in paragraph 1.

Not: *"first_order_coherence = 0.31 (p8)."* That is a number a writer can neither picture nor
act on.

## Interpreting honestly

**A percentile is a question.** An index falls outside the band for two reasons that look
identical in the output: the draft is doing something readers will struggle with, or the
draft is doing something the corpus does not do for reasons of genre, section, or topic. Read
the passage before reporting the number. If you cannot find the passage the number points at,
do not report the number.

**These instruments were validated for other purposes.** The cohesion and complexity indices
were developed and validated largely against comprehension outcomes, essay quality ratings,
and L2 proficiency — not against "will an expert reviewer find this contribution valuable."
Treating them as a proxy for the second is a real inferential leap, and the honest move is to
make the leap visible rather than hide it behind a percentile. The author is likely to know
this literature better than you do; where they push back on an index's relevance, they are
probably right.

**Lexical diversity deserves particular caution.** taaled's MATTR, MTLD and HD-D are
proficiency and development measures. In expert academic prose a *low* score usually reflects
consistent technical terminology — exactly what the code layer wants. Reporting it as a flaw
would be actively bad advice. Report it only when the author asks, and say what it does and
does not license. See `references/index-map.md` §4.

**Never average indices into a composite score.** They are correlated, differently scaled and
differently valid. A composite is uninterpretable and lends false authority to everything
around it.

## Resources

- `references/index-map.md` — which index bears on which diagnostic question, Tier 1 and
  Tier 2, with the validity caveats. **Read before interpreting any output.**
- `references/setup.md` — installation for both tiers, known breakages, TAACO's missing files.
- `scripts/doctor.py` — environment check and tier recommendation. Run first, every time.
- `scripts/tcm.py` — stable cross-skill launcher; discovers the venv and combines measuring
  with building/comparing norms.
- `scripts/run_tools.py` — unified runner across both tiers; emits a tidy CSV tagged with
  backend, version, spaCy model, and tier.
- `scripts/norms.py` — build percentile norms from a corpus; compare a draft against them,
  with a provenance guard against cross-tier comparison.
- `requirements-tier1.txt` — tested, pinned Python 3.10–3.12 environment, including the
  vector-bearing English model required for coherence.
- `requirements-tier2-core.txt` — the small additional dependency used by the local TAASSC
  source tree; TAASSC also requires its hardcoded transformer model.
