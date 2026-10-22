# Benchmark & evolution

> Read this before quoting any number from the README. It records the benchmark design, the measured
> results, the package's version-by-version evolution, and what remains unproven.

## TL;DR

- The package was benchmarked on **two constructed argument-damage cases**: real papers whose prose is
  left untouched and whose *argument* is damaged (buried contribution, gap opening, broken paragraph
  handoffs, limitations spliced into live claims, implication before evidence).
- Current version **1.2.5**: property-span v2 **1.00 ×4 artefacts** on the working case; review scorer
  **3/3 ×4 artefacts** on the hard review case; under a **same-prompt controlled comparison** it scores
  **2.500 / 3** against the strongest characterised competitor's **0.250 / 3** (15 wins, 1 tie, 0 losses
  in 16 cross-artefact pairs).
- The deterministic screens were validated against the metrics: **25/25** (abstract property) and
  **29/29** (introduction-close property).
- **What this is not:** no effect size, no ranking, no human anchor; two constructed cases and one model
  family; one blind-reader pair went to a competitor. Read the limits section before quoting anything.

## How it was measured

**Cases.** Two cases built from post-horizon preprints so the material cannot be recalled from training
data (a contamination probe was run on the working case).

| case | source | what was damaged |
|---|---|---|
| working case | arXiv:2610.03827, de-extracted with structure restored and prose byte-identical | six argument-level moves: contribution buried, gap opening, six handoffs broken, four limitations spliced into claims, implication before evidence, two transitions deleted |
| hard case | arXiv:2610.01938 (clinical-reasoning review) | the same damages, scaled to touch **78% of prose paragraphs**, so the arms cannot converge |

**Arms.** This package against characterised competitor packages, all cloned at pinned commits:
academic-research-skills (ARS), anti-defensive-writing, PaperSpine, nature-skills,
research-paper-writing, research-writing-zh, humanizer, plus an unaided rewrite. Same model, same task
prompt, one fresh agent per artefact, byte-identical source in every arm directory.

**Rigor rules.** Every artefact is frozen with sha256 before scoring. Distributions are reported, never
a single draw (four artefacts per arm where capacity allowed). Package edits are **pre-registered** with
an acceptance rule and a revert rule fixed before the run, and measured on fresh artefacts only. Judged
comparisons are dual-order with an agreement filter and a reported flip rate. Instruments are
hash-checked and calibrated against known-good/known-damaged references before use.

**Metrics.** Two calibrated objective instruments (each anchored so the clean reference = 1.0 and the
damaged draft = 0.0):

- **property-span v2** (working case): A1 abstract states a finding and carries no gap framing;
  A2 the introduction's close carries the answer; A4 no asserted caveat inside Results.
- **review scorer B1/B2/B3** (hard case, no Results section exists): B1 abstract carries no gap framing;
  B2 the introduction closes on the review's answer; B3 limitations live in one place.
- **deterministic screens** (shipped): `scripts/argument_screen.py` implements the same surfaces as
  checks a user can run in two seconds.

## Results

### Working case — property-span v2 (standard prompt)

| arm | artefacts (v2) | mean | deterministic screen |
|---|---|---|---|
| **this package, 1.2.4–1.2.5** | **1.00, 1.00, 1.00, 1.00** | **1.000** | **4/4 pass** |
| this package, 1.2.3 (A1 edit) | 0.833 ×4 | 0.833 | 4/4 pass |
| this package, 1.2.1 (pre-edit baseline) | 1.00, 0.83, 0.67, 0.67 | 0.792 | 4/4 pass |
| ARS | 0.00 ×4 (batch); 1.00 in one earlier draw | 0.000 | 0/4 |
| anti-defensive-writing | 0.33, 0.67 | 0.500 | 0/2 |
| PaperSpine | 0.00, 0.00 | 0.000 | 0/2 |
| nature-skills · research-paper-writing · research-writing-zh · humanizer · unaided rewrite | 0.00 (one artefact each, round 1) | 0.000 | fail |

The working-case metric is **saturated** for this package (four draws at the top of the span). It still
separates arms — the competitors are all far below — but it cannot measure further improvement by this
package.

### Hard review case — review scorer B1/B2/B3 (standard prompt)

| arm | artefacts (surfaces passed of 3) | mean | B1 | B2 | B3 |
|---|---|---|---|---|---|
| **this package, 1.2.4–1.2.5** | **3, 3, 3, 3** | **3.000** | **4/4** | **4/4** | **4/4** |
| this package, 1.2.2 (pre-edit baseline) | 2, 2, 2, 1 | 1.750 | 3/4 | 2/4 | 2/4 |
| ARS | 1, 0, 0, 0 | 0.250 | 0/4 | 0/4 | 1/4 |

### Controlled comparison — same instruction for both arms (diagnostic prompt)

When both arms were given the *same* "this is a full argument revision, repair at full depth"
instruction on the hard case:

| arm | artefacts (of 3) | mean | B1 | B2 | B3 |
|---|---|---|---|---|---|
| this package, 1.2.5 | 1, 3, 3, 3 | **2.500** | 4/4 | 3/4 | 3/4 |
| this package, 1.2.4 (pre-scope-edit) | 2, 2, 2, 1 | 1.750 | 4/4 | 3/4 | 0/4 |
| ARS | 0, 0, 0, 1 | 0.250 | 0/4 | 0/4 | 1/4 |

Cross-artefact pairs between the package batch and the ARS batch: **15 wins, 1 tie, 0 losses in 16**.
Median word-sequence similarity between the two batches: **75.0%** — below the 88% threshold the project
uses for judge-visible divergence, i.e. this comparison is visible to a human or judge reader.

The diagnostic instruction also explains the ARS batch split: ARS re-emitted 10,787-word revisions and
still failed to repair the measured surfaces (0.250, exactly its standard-prompt mean). The same skill's
single earlier 1.00 draw was not reproducible under explicit instruction on either case.

### Screens validated against the metrics

| screen | agreement with its metric on frozen manuscripts |
|---|---|
| screen A — abstract states a finding, no gap framing | **25/25** (opening-only rule: 20/25) |
| screen B — introduction's closing sentence carries the answer | **29/29** (paragraph rule: 21/29) |
| screen C — limitations vs claim calibrations | separates them; clean reference exits 0, damaged draft exits 1 |

## Version evolution (every step measured)

| version | change | what it fixed |
|---|---|---|
| 1.0.0 | two-pass architecture (reader layer, then audit) | an earlier merged version that checked while drafting scored **6 wins to 42** against an unaided rewrite |
| 1.1.0 | put the answer where readers look (abstract + introduction close) | replies were repaired but the answering sentence sat in the Discussion |
| 1.2.0 | deterministic `argument_screen.py` | two runs each missed one reader surface; the screen catches them in two seconds |
| 1.2.1 | separate limitations from claim calibrations in the screen | a legitimate calibration sentence in Results was being treated as a limitation |
| 1.2.3 | abstract may not carry gap framing anywhere | 2 of 4 artefacts left a gap sentence after the opening (A1 2/4 → 4/4) |
| 1.2.4 | the introduction must close on the answering sentence | answer sat inside the closing paragraph but ended on evidence (A2 0/4 → 4/4) |
| 1.2.5 | scope statements are limitations | under a full-revision instruction the body kept an operational-definition scope sentence (B3 0/4 → 3/4) |

Two-release documentation/evidence updates (1.2.2) changed no behaviour. The rule that produced every
version: **one edit per round, pre-registered, measured on fresh artefacts, reverted if its own
acceptance rule failed.** Adding guidance without a verified defect made the package worse in earlier
rounds (recorded in `EVIDENCE.md`).

## The reader-preference record

Blind, dual-order, agreement-filtered judging with a same-model-family second reader:

| pair | pair type | result |
|---|---|---|
| package vs ARS (frozen draw) | judge-visible headroom | **package preferred 5–0** on agreed dimensions; 17% order-dependent; low/high deliberation agreement 5/5 |
| package vs ARS (hard case, two ~95%-identical revisions) | no headroom | **unresolved** — 33% and 17% flips, deliberation conditions pointed in opposite directions |
| package vs anti-defensive-writing (headroom) | judge-visible headroom | **competitor preferred 3–1 / 4–1** on flow, interest, overall; package kept logic in both conditions; low/high agreement 4/4 |

Earlier single-pair dual-order judging on the 1.2.1 artefact preferred it to ARS 5–1 and to
nature-skills 6–0 (0% order-dependent on both pairs), was undecided against PaperSpine 3–3, and did not
establish an order against anti-defensive (50% order-dependent). The same-family second reader is
**not an independent or human anchor**, and it is not package-biased (one headroom pair went to a
competitor).

## What this benchmark does *not* establish

- **No effect size.** Two constructed cases, one model family, one to four artefacts per arm.
- **No ranking.** The package is at the measured ceiling on both cases and ahead of the strongest
  characterised competitor under both prompts, but there is no stable ranking and no magnitude.
- **No comprehensive reader superiority.** The package is strongest on the measured argument surfaces;
  a competitor's revision was preferred on one judge-visible reader pair.
- **No generalisation beyond constructed cases.** Both cases are built from post-horizon preprints;
  naturally written drafts carry no sentence-level writing headroom (measured: six methods produced
  90.9–92.5%-identical documents and judging measured noise).
- **No independent or human anchor.** Local and frontier-model attempts failed (the local 7.5B judge was
  retired at 75% order-dependence); human raters remain the strongest untried anchor.
- **A single artefact is a draw, not an estimate.** Within-arm runs span 0.67–1.00 on the pre-edit
  package, and the same competitor commit produced 0.00 and 1.00 in different batches.

## Where the numbers live

- **`EVIDENCE.md`** — the full measurement record: judge protocol and its faults, case construction
  and gates, metric definitions and the instrument errors that led to them, overturned claims, and the
  published settings. It is the source of every number above.
- The research apparatus (case de-extraction and damage scripts, arm run directories, freeze manifests,
  metrics, judges, and the gen-numbered round reports) lives in the author's separate research
  repository. Public paths such as `bench/...` referenced inside `EVIDENCE.md` refer to that apparatus.

## Reproduce the checks on your own draft

```bash
python scripts/argument_screen.py DRAFT.md   # return code 0 = no flags; 1 = at least one flagged surface
python scripts/intake_screen.py DRAFT.md     # mechanical floor: placeholders, missing sections
python scripts/check_manuscript.py DRAFT.md --profile project/venue-target.md
python scripts/prose_lint.py DRAFT.md
```

A flag is a prompt to read the printed sentence, not a verdict; a clean run is not a passing argument
review.
