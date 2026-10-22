# Evidence

> **This is the full measurement record.** A shorter, reader-friendly summary of the benchmark and of
> the package's version-by-version evolution is in [BENCHMARK.md](BENCHMARK.md). Paths written as
> `bench/...` refer to the author's separate research apparatus, where the raw artefacts, case builds
> and gen-numbered round reports live; every number needed to read this file is stated here.

Every number in [BENCHMARK.md](BENCHMARK.md) and in the README comes from here. This file records what
was measured, how, what was overturned, and which parts of the measurement apparatus failed — because
in this project the apparatus was the most frequent source of wrong conclusions.

## The comparison

Three arms, same model, same task, same source manuscript:

| arm | what it is |
|---|---|
| **shu-academic-writing-skill** | this bundle |
| alternative skill | an existing open-source academic-writing skill, cloned at a pinned commit |
| no method | a plain instruction to revise the manuscript for submission |

Artifacts are frozen with sha256 before any judging. Arms alternate sides across pairs so that an
additive position bias cancels in the mean.

## The judge protocol

1. **Forced choice, no "equal" option.** Six questions: logic, flow, interest, comprehension, pleasure,
   overall. A rating would hide what it was compared against.
2. **Blinded.** Judged on files named `X.md` and `Y.md`; the key lives outside the judge directory.
3. **Dual order.** Every pair is judged twice, with the arms swapped, by different judges.
4. **Agreement filter.** A question counts only when the *same arm* wins in both orders. Questions that
   flip are recorded as order-dependent and excluded.
5. **Transitivity check.** Round-robin over three arms, exhaustively testing whether any ordering
   satisfies all pairwise results.
6. **Bradley–Terry.** Strengths fitted by MM, with a bootstrap interval, instead of counting wins.

### Why the protocol looks like this

It was repaired twice, each time because a result was implausible:

- **Order reversal is mandatory** because 50% of question-level verdicts reverse when the same pair is
  read in the opposite order, and two of three measured pairs had their *winner* flip — one from 1–5 to
  5–1. After every pair was run both ways, order-dependence fell to 25–29%.
- **The tell had been visible four times** before it was measured: an identical question-by-question
  pattern in judgments whose arms had swapped sides. A pattern that does not move when the arms swap is
  not measuring the arms.

## Results

Blinded forced choice, agreement-filtered:

| comparison | case | result |
|---|---|---|
| shu-academic-writing-skill vs alternative skill | cognitive-science paper | **6 – 1** agreed questions, 2 of 2 pairs |
| shu-academic-writing-skill vs alternative skill | philosophy-of-mind paper | **9 – 0** agreed questions, 2 of 2 pairs |
| shu-academic-writing-skill vs no method | cognitive-science paper | **11 – 5**, 3 of 4 pairs |
| shu-academic-writing-skill vs no method | philosophy-of-mind paper | **13 – 4**, 3 of 4 pairs |

Under a **reader** framing, an earlier standalone version of the reader layer scored 29–7; under a
**reviewer** framing, 11–1.

Bradley–Terry over 30 agreed-question observations:

```
shu-academic-writing-skill          0.722                      baseline
alternative skill  0.163   [-3.38, -0.53]     ≈4.4× weaker
no method          0.115   [-4.27, -0.65]     ≈6.2× weaker
transitive: shu-academic-writing-skill > alternative skill > no method
```

**The finding the win counts hid:** the two baselines are *not distinguishable from each other*. Their
intervals overlap almost completely. The honest form is `shu-academic-writing-skill > { alternative skill ≈ no method }` —
three arms, two rungs.

## What was overturned

Recorded because a package whose evidence file only lists its wins is not evidence.

| claim | status |
|---|---|
| "carrying compliance rules into drafting improves the paper" | **false** — 6 wins to 42 against an unaided rewrite |
| "the module can be fixed by reordering its four delivery steps" | **false** — three redesigns moved the control comparison by zero |
| "quarantining disclosures into one block fixes readability" | **false** — the interruption changed address, from scattered caveats to a 350-word wall |
| "a third pass that integrates the audit's corrections helps" | **false** — 16–8 became 8–16, and it *deleted* corrections |
| "pointer-thin disclosure is better than verbose" | **false** — 10–14; a pointer at an analysis the paper does not contain is a promise |
| "judges prefer ornate prose" | **false** — every probe preferred plain over ornate at identical content |
| "the problem-framing module improves judged quality" | **not shown** — 6–6; it is included for compliance only |
| "the two baselines differ" | **not shown** — intervals overlap |

## Instrument errors

Twenty-two, all found by inspecting raw output after a number looked wrong. Grouped by kind, because
the kinds are the lesson:

- **Shadowing and schema faults** — a bench file named `inspect.py` breaking stdlib imports; a
  schema-dependent scorer that inverted the ranking because both real skills imposed their own output
  shape.
- **Scopes applied to the wrong object** — a word limit meant for front/back matter applied to the whole
  document; a heading regex accepting `## Abstract` but not `**Abstract**`.
- **Thin validation, silencing false positives and negatives** — a reference-list check that rejected a
  valid list; a placeholder check that missed angle-bracket names.
- **Items that failed everything, or nothing** — a mechanical check that flagged all 21 artifacts for a
  true statement, and four checks that no artifact ever failed.
- **Capturing artifacts mid-write** — fixed by requiring repeated mtime stability before freezing.
- **Thresholds pulled out of the air** — a 45–95% text-overlap window that rejected a *correct*
  extractor, because a heavy rewrite legitimately falls outside it. Replaced by paragraph
  correspondence, which can distinguish a rewrite from a broken parser.
- **A gate that rejected good cases** — a PDF fitness gate that rejected a 21→23 page theory paper over
  one extra mention of "Study 2". Replaced by a requirement for *material* growth.
- **A self-comparison fit** — the first Bradley–Terry run returned a strength of exactly 0.000 for this
  bundle; the observations had been recorded as `(arm, arm)` because the agreement filter had just
  established both orders picked that arm.
- **A metric that counted words, not claims** — property-span P4 counted "each is a test we can run
  rather than **a caveat** we can add" as a caveat: a sentence that names the concept in order to deny
  it. The fix (gen 62) excludes a marker immediately preceded by a negation/rhetorical cue and keeps
  the clean/degraded calibration; one cell changed, ours × P4, 0.00 → 1.00.
- **A property list calibrated once, then trusted** — applying property-span v1 to a *second run* of
  the same package exposed two definition errors: P1 counted first-person finding verbs only (a
  declarative abstract that states findings scored zero), and P2's window was the last two sentences
  while the rule's window is the last paragraph. P3's clean-versus-damaged gap (0.327 vs 0.292) was
  smaller than its movement between two runs of one method (0.355 vs 0.282). v2 (gen 62b,
  pre-registered before scoring) keeps only damage-tied properties with a real calibration gap and
  reports P3 as a diagnostic.
- **One artefact per arm treated as an estimate** — the same package on the same case produced 0.67
  (run24) and 0.08/0.50 (run30, working-case re-run) by v1/v2 because the two runs repaired different
  defective sites. Round 2 quantified it: four fresh artefacts of the final package span 0.67–1.00 on
  v2 (mean 0.79), and within-arm text similarity is 77–87%.
- **Treating an arm as one stable procedure** — the same ARS skill commit scored 1.00 on one run and
  0.00 on four fresh runs; its own report in the zero batch says the skill's "revision mode" was
  applied as a *contained editorial pass* because no reviewer comments existed, while the 1.00 run
  enumerated and repaired all six argument faults. The application mode is part of the arm, and
  between-batch variance can exceed the between-package difference. No ranking against ARS is claimed
  until that split is explained.
- **A weak independent model treated as an anchor** — round 2 built the missing independent-family
  judge (`bench/gemini_judge.py`, local Gemma-family 7.5B via Ollama) after frontier Gemini proved
  unavailable. It produced all eight blinded verdicts but was order-dependent on 75% of dimensions
  (same-family: 12%) and resolved only 6/24 itself; on the 4 dimensions both families resolved it
  agreed 4/4 (17% coverage). An independent estimator must have its own stability measured before it
  is called an anchor.

**The mechanism that caught every one of them is the same:** a printed number that could not be true.

## Gate criteria for new test material

If you extend this benchmark, material must pass five gates before it produces a number. `README.md`
claims only what passed all five.

| gate | rule |
|---|---|
| revision gap | **3–21 days.** A long gap is when authors add studies; a short one is when they fix and rewrite. Filtering for ≥20 days produced only evidence revisions. |
| revision type | tables, figures, equations and page count must not outgrow the text. Mechanically checked, HTML or PDF. |
| extraction | same opening, ≥50% paragraph correspondence between the two versions, no page-scraper chrome. |
| contamination | post-horizon material only, verified by a blind probe: remove values or short spans and ask for restoration with no search, where `unknown` costs nothing and a guess is a miss. |
| subject matter | **read the abstract.** This one is not automatable — a lexical proxy passed an LLM-architecture paper as psychology, because AI papers use *memory*, *attention* and *cognitive* as heavily as psychology papers do. |

## The constructed case (2026-10-22)

The natural-material search failed: every post-horizon preprint that passed the gates was competently
written at sentence level, so every method produced effectively the same document and judging measured
noise (gen 54/56). The case that finally discriminated was constructed (gen 58/59):

- **Source.** arXiv:2610.03827, post-horizon, de-extracted as preprocessing with structure restored and
  prose untouched: 95.3% word similarity to the bare extraction, 254/267 sentences byte-identical.
- **Damage.** Six argument-level moves: bury the contribution; open on a gap; break six paragraph
  handoffs; interleave four limitations into the claims they qualify; put implication before evidence;
  delete two cross-section transitions. No sentence rewritten; 20 sentences moved or deleted plus two
  inserted gap framings; a script that strips the logged sentences from both files leaves identical
  remainders; the rebuild is deterministic.
- **Why it is usable.** Four arms diverge (median pairwise word similarity 83.2%, below the 88% line),
  and a pure style tool that reproduced the source 92.3% still loses 5–0 on preference, because it
  repaired the sentences around six intact argument defects.

## What the current version does on it

Property-span v2 (gen 62b: three properties tied to the planted damages, calibrated clean = 1.00,
damaged = 0.00; the unreliable P3 is reported as a diagnostic and excluded). Round 1 ran one artefact
per arm; round 2 ran four fresh artefacts for this package and ARS, two for anti-defensive and
PaperSpine. **The distribution is the result; a single artefact is a draw.**

| arm | version | artefacts (v2) | mean | screen pass |
|---|---|---|---|---|
| **this package** | **1.2.1** | **1.00, 0.83, 0.67, 0.67** | **0.79** | **4/4** |
| ARS (academic-research-skills) | cfd081d | 0.00, 0.00, 0.00, 0.00 (round 2); single run 1.00 (run24) | 0.00 | 0/4 |
| anti-defensive-writing | 82d3140 | 0.33, 0.67 | 0.50 | 0/2 |
| PaperSpine | 42312b8 | 0.00, 0.00 | 0.00 | 0/2 |
| nature-skills, research-paper-writing, research-writing-zh, unaided rewrite, humanizer | — | 0.00 each (round 1, one artefact) | — | fail |

Round 1's single-artefact version trajectory remains the provenance of the method: 1.0.0 → 1.1.0
(answer-placement rule) → 1.2.0 (deterministic screen) → 1.2.1 (the screen separates limitations from
claim calibrations). The final version's four artifacts are the only set in which every run passes the
deterministic screen. The ARS split is reported, not smoothed: the same skill can be applied in a mode
that repairs the measured surfaces and one that does not, so **no ranking against ARS is established**
by this table. Artefacts are frozen with sha256 in `bench/revision_runs32/`, `revision_runs33/`.

The same screen, run on the frozen artefacts (a screen, not a score): the clean reference exits 0;
the damaged draft exits 1 with all three flags; all four 1.2.1 artefacts exit 0; every other
characterised arm/fresh run exits 1. Reproduce:

```bash
python scripts/argument_screen.py DRAFT.md
```

A blinded dual-order judge on the 1.2.1 artefact (four pairs, both orders, agreement filter) preferred
the package to ARS 5–1 and to nature-skills 6–0 with 0% of dimension verdicts order-dependent on either
pair, was undecided 3–3 against PaperSpine, and did not establish an order against anti-defensive
(50%). That is same-family, single-pair-per-competitor, direction only.

## The second and third cases — one converged, one now usable

A second constructed case (arXiv:2610.01938, clinical-reasoning review; gen 65) was validated in full
but its two arms converged at 90.3% word similarity — too localised in an 8,500-word body — and was
recorded as a negative result.

Round 2 built a **harder** variant from the same byte-identical clean source: all 21 earlier
moves/deletes plus enough damage to touch **35 of 45 prose paragraphs (78%)**; 16 moved, 27 deleted, 2
labels deleted, 2 gap framings inserted; strip-log remainder identical, 411/440 sentences survive
verbatim with 0 unexplained, deterministic rebuild, five material gates pass. Four fresh artefacts
(2 this package, 2 ARS) give cross-arm word similarity 69.7 / 71.5 / 89.4 / 94.5 → **median 80.43%,
below the 88% line: usable**. A pre-registered review-genre scorer (B1 abstract contains no gap
framing; B2 introduction closes on the review's answer; B3 limitations live in a limitations section)
calibrates clean 3/3 and damaged-hard 0/3; on it the package scores **4/6** (runs 1/3, 3/3) and ARS
**1/6** (1/3, 0/3) — a direction on n=2, not a result. Frozen hashes in
`bench/revision_runs34/frozen/MANIFEST.json`; report gen 68.

## The independent estimator — attempted, still open

Round 2 tried the project's missing independent anchor (gen 69). Frontier Gemini was unavailable
(model list reachable, then 503/429 quota; retired ids 404; full workload did not return). A local
Google-Gemma-family judge (7.46B, `bench/gemini_judge.py --backend ollama`) produced all eight blinded
order-dir verdicts against the package-1.2.1 pairs — but was order-dependent on **75%** of dimensions
and resolved only 6/24; where both families resolved a dimension they agreed 4/4 (17% coverage).
A second family (Qwen3-VL-8B) was unusable. **The local-model pilot is retired** (the user judged it
poor, and its 75% order-dependence agrees): the next protocol is a same-family **subagent low/high
blind review** — two fresh subagent readers per pair at low and high reasoning-effort, both orders,
with low-vs-high agreement as the deliverable (recipe in the research repo's `bench/JUDGING-PROTOCOL.md`)
— while human raters or a frontier independent model remain the stronger anchor. **The
independent-anchor question remains open**, and no preference claim rests on it.

## What would settle the open questions

In the order the evidence justifies:

1. **Multi-artefact on the hard case.** The hard case discriminates and has a pre-registered scorer;
   4–6 artefacts per arm there is the cheapest second-case distribution and the route to a real
   between-case effect size.
2. **An independent or human anchor.** Frontier-model judging (client ready) or human raters on a
   subset, with the judge's own order-dependence measured and reported first.
3. **Explain the ARS batch split** (1.00 vs 0.00): rerun the same skill with an explicit fault diagnosis
   to test whether the full-repair mode is reproducible. Until then the fair comparator is ambiguous and
   no ranking against it is claimed.
4. **One candidate package edit, only if a batch confirms it:** 2 of 4 package artefacts left an
   unhedged gap sentence in the abstract (A1 = 0) while opening on a stake; the clean reference keeps
   it in §1.1. If confirmed, extend the reader-layer rule and screen A so gap framing belongs in
   Related Work, not the abstract. One edit, pre-registered, measured on the next batch.
5. **Not more modules.** Adding guidance, reordering steps and re-tuning thresholds each produced zero
   new information across many rounds. The two changes that did work were a placement rule and a
   deterministic check.

**Status after round 3:** item 1 (multi-artefact hard case) is done (gen 71); item 3 (ARS batch
split) is explained as far as instruction can explain it — the full-repair instruction does not
reproduce the 1.00 (gen 72); item 4 (the candidate A1 edit) is shipped and measured (gen 73, package
1.2.3); item 2 (independent anchor) has a working same-family subagent protocol but still no
independent family or human anchor (gen 74); item 5 is unchanged — round 3 added no module.

## Round 3 — the second case as a distribution, the ARS mode diagnostic, one measured edit, and a subagent reader

All of round 3 was pre-registered before measurement (\`bench/PRE-REGISTRATION-ROUND3.md\` in the
research repo); decisions below follow the pre-registered rules, and every departure is logged in the
named report.

### The hard case as a distribution (gen 71)

Case \`2610.01938-hard\` (clinical-reasoning review; damage touches 78% of prose paragraphs), its
gen68 pre-registered scorer (B1 abstract carries no gap framing; B2 introduction closes on the
review's answer; B3 limitations live in one place), four fresh artefacts per arm, package frozen at
1.2.2 to keep the round-3 edit out of this measurement.

| arm | artefacts (surfaces passed of 3) | mean | B1 | B2 | B3 |
|---|---|---|---|---|---|
| this package | 2, 2, 2, 1 | **1.75** | 3/4 | 2/4 | 2/4 |
| ARS (cfd081d) | 1, 0, 0, 0 | **0.25** | 0/4 | 0/4 | 1/4 |

The pre-registered rule was fixed before data: claim a favourable second-case direction only if the
package beats ARS in **≥12 of 16** cross-artefact pairs. Measured: **15 wins, 1 tie, 0 losses.** The
case still discriminates (12 frozen artefacts, median cross-arm word similarity 83.89% < 88%), though
8 of 16 cross pairs sit at or above 88% — reported with the result. Residual package misses: one
abstract keeps the planted gap sentence, two artefacts leave one limitation statement in the body, and
two answers do not match the B2 formula (recorded as conservative-formula misses, not content
failures). The review scorer's section identification was repaired mid-round (heading-numbering
agnostic; rules unchanged; gen68's four artefacts re-score identically) — logged in gen71 §8.

### ARS's application mode, tested (gen 72)

Round 2's same-commit ARS split (1.00 in run24, 0.00 ×4 in run33) was attributed to ARS running its
revision mode as a contained editorial pass. Round 3 told each arm, identically, that this is a full
argument revision and to diagnose and repair at full depth. ARS escalated to a full 10,787-word
re-emission — and still scored **0.00 and 0.33** (mean 0.167), closing the introduction on roadmaps
("Section 6 concludes.") and leaving caveats in Results. The package under the same instruction scored
**1.00 and 0.83** (mean 0.917) and passed its screen 2/2. Diagnostic only, n=2: the instruction-driven
explanation is not supported; run24's 1.00 is an outlier at current evidence, and no package-vs-ARS
ranking is claimed from either prompt.

### The A1 edit, measured (gen 73; package 1.2.3)

Defect (gen 67): 2 of 4 package artefacts left a gap sentence after the abstract's opening while
passing the old screen, which only checked the first two sentences. The edit extends the reader-layer
rule to the whole abstract and tightens screen A to match; the tightened rule was validated before the
run on **25/25** frozen empirical-case manuscripts against the v2 A1 property (the old rule: 20/25).
Four fresh post-edit artefacts: **A1 4/4** (was 2/4), property-span v2 **0.833 ×4** (mean 0.833, was
0.792), tightened screen **4/4 exit 0**, A4 at the clean reference's level 4/4. Two honest caveats:
the pre-registered A4 "pass count" was mis-specified — its raw threshold also fails the clean
reference, so the intent reading (A4 span = 1.00 on 4/4) is what is claimed, with both readings in the
gen73 report; and A2 moved from the introduction's closing **sentence** (3/4 before) to inside the
closing **paragraph** (0/4 final sentence, 4/4 paragraph), lowering the secondary v1 metric to 0.550
against a 0.60 guide. The edit was kept because its target is verifiably fixed at no v2 or screen
cost; the A2 clarification is a pre-registered candidate for one future round.

### A same-family subagent blind review (gen 74)

User-directed protocol: four fresh subagent judges on one frozen pair (package run33 draw, v2 0.67, vs
ARS run33 draw, v2 0.00), {both orders} × {low, high deliberation instructions}, blinded, scored with
the dual-order agreement filter. Result: **5 of 6 dimensions resolved, the same arm won in both orders
and both deliberation conditions (package 5–0), 17% of dimension verdicts order-dependent** (pleasure
only, a position effect: both conditions picked the second document), and **low-vs-high agreement 5/5**
on the co-resolved dimensions. For comparison, the retired 7.5B local judge on round-2 pairs was 75%
order-dependent and resolved 6/24. This is a working second-reader protocol and **not an independent
anchor**: same model family, one pair, direction only. The deliberation conditions are a substitution
for a harness effort setting that does not exist here, and are labelled as such.

### Still open after round 3

- **No independent-family or human anchor.** The subagent protocol is stable but same-family.
- **The A2 placement question.** One pre-registered edit can clarify whether the introduction's closing
  sentence must carry the answer; the current rule leaves that to the writer, and the post-edit batch
  chose the paragraph-first form.
- **A mode-controlled comparison at n≥4 per arm** (the diagnostic was n=2 and not a ranking).
- **No effect size, no generalisation beyond two constructed cases.**

## Round 4 — the A2 edit at the ceiling, and a blind-review protocol with a measured operating range

### The A2 placement edit, measured (gen 76; package 1.2.4)

Defect: after round 3's A1 edit, four fresh artefacts put the answer **inside** the introduction's
closing paragraph and ended that paragraph on evidence — property-span A2 = 0.5 on 4/4 (the pre-edit
batch had 3/4 closing-sentence placements), v1 fell to 0.550 against a 0.60 guide. The rule said the
introduction's close must carry the answer but not that the closing sentence must; screen B only
checked the paragraph.

The edit (one behaviour change): the reader-layer rule and the two-minute test now require the
introduction's last paragraph to **close on** the answering sentence, and screen B checks the closing
sentence. Instrument validation before the run: on 29 frozen empirical-case manuscripts the tightened
screen agrees with v2 A2 = 1.0 on **29/29** (the paragraph rule: 21/29); clean reference passes,
damaged draft fails.

Four fresh artefacts, standard prompt, working case: **A2 closing-sentence pass 4/4** (was 0/4),
property-span v2 **1.00 ×4** (mean 1.000; was 0.833), tightened screen **4/4 exit 0**, A1 still 4/4,
v1 **0.723** (was 0.550; pre-edit 0.732). All four pre-registered acceptance criteria passed; the edit
is kept. **The working-case metric is now saturated** for this package — four draws at the top of the
calibrated span — so it becomes a regression test and further package edits must be measured on the
hard case or a new case.

### The blind-review protocol on a second pair (gen 76; pre-registered negative result)

The same same-family subagent low/high protocol as round 3, on a second frozen pair from the hard
case (package review-scorer 3/3 vs ARS 1/3; the two revisions are ~95% identical). Low deliberation:
4/6 dimensions resolved, **package 4–0**, 33% order-dependent. High deliberation: 5/6 resolved,
**ARS 4–1**, 17% order-dependent. Low-vs-high agreement: **1 of 4** co-resolved dimensions; the two
conditions point in **opposite directions**. Pre-registered verdict: **the pair is not resolvable by
this protocol.**

Measured rate: two pairs, one resolved (round 3: 5/6, package 5–0 both conditions, low-vs-high 5/5)
and one not (this round). The protocol is a second reader for pairs with **judge-visible headroom**;
it is not an anchor, and it must not be used on near-identical pairs or averaged across deliberation
conditions. Its use in this project's claims is limited to that statement.

### Still open after round 4

- No independent-family or human anchor; the subagent protocol's operating range is now measured.
- The hard case has not been re-measured under package 1.2.4 (the gen71 distribution used 1.2.2).
- No mode-controlled package-vs-ARS comparison at n≥4 per arm; no effect size; no generalisation
  beyond two constructed cases.

## Round 5 — both edits generalise, the hard case saturates, and ARS's mode conclusion replicates

### The A1/A2 edits on the hard review case (gen 77; package 1.2.4, no edit this round)

Four fresh package-1.2.4 artefacts on `2610.01938-hard` under the standard prompt, scored with the
pre-registered review scorer (B1 abstract carries no gap framing; B2 introduction closes on the
review's answer; B3 limitations live in one place): **3/3, 3/3, 3/3, 3/3 — mean 3.000**, B1 4/4,
B2 4/4, B3 4/4. Against the gen71 baseline of package 1.2.2 (2/2/2/1, mean 1.75; B1 3/4, B2 2/4,
B3 2/4), all three pre-registered generalisation criteria passed, and the two edited rules are exactly
the two surfaces that moved (B1 and B2). Against the frozen ARS batch on the same case: 16/16
cross-artefact pairs (pre-registered rule ≥12/16). Pooled package hard-case distribution (n=8):
3,3,3,3,2,2,2,1 — mean 2.375. **Both constructed cases are now saturated for this package** on their
pre-registered scorers; they are regression tests, not improvement instruments.

Caveat that travels with the 16/16: word-sequence similarity between the package and ARS batches on
this case has median **93.8%**, above the 88% line the project uses for judge-visible divergence. The
objective scorer still separates the arms (3.00 vs 0.25) because it reads the planted surfaces; the
batch is not judge-visible and must not be used in a preference comparison.

### ARS under the explicit full-revision instruction, on the review genre

Four fresh ARS (`cfd081d`) artefacts on the same hard case under the gen72 diagnostic instruction:
**0, 0, 0, 1 — mean 0.250**, identical to ARS's standard-prompt mean on this case (1,0,0,0 → 0.250),
and B1 0/4, B2 0/4, B3 1/4. The artefacts grew 7–18% and their change logs diagnose 16–26 defects, so
the instruction changed ARS's *behaviour* but did not repair the measured surfaces. This is the second
case on which the gen72 conclusion replicates: the run24 full-repair draw is not reproducible by
instruction. Secondary pre-registered bound: package standard-prompt artefacts beat ARS's
instructed artefacts 16/16 cross-pairs — a bound generous to ARS, not a ranking.

### Still open after round 5

- No ranking, effect size, independent or human anchor (unchanged).
- A mode-controlled package-vs-ARS comparison on the hard case is the one remaining comparator
  measurement (package 1.2.4 under the diagnostic prompt ×4 against the run40 batch).
- Both existing scorers are saturated for this package: further package work needs a new case or a new
  surface.

## Round 6 — the mode-controlled comparator, a mode-fragility finding, and a blind-review pair the competitor wins

### Mode-controlled package-vs-ARS comparison (gen 78; hard case, both arms under the diagnostic prompt)

Four fresh package-1.2.4 artefacts on `2610.01938-hard` under the same diagnostic instruction as
run40 (ARS, same case, n=4), scored with the pre-registered review scorer:

| batch | totals | mean | B1 | B2 | B3 |
|---|---|---|---|---|---|
| package 1.2.4 | 2, 2, 2, 1 | **1.750** | 4/4 | 3/4 | 0/4 |
| ARS cfd081d | 0, 0, 0, 1 | **0.250** | 0/4 | 0/4 | 1/4 |

Controlled cross-pairs: **15 wins, 1 tie, 0 losses** in 16 — the pre-registered ≥12/16 threshold is
passed. Median word-sequence similarity between the batches is **75.0%** (below the 88% visibility
line), so this comparison is judge-visible.

**Pre-registered mode-fragility finding.** The same package scores **3.000/3** under the standard
prompt on this case (run39) and **1.750/3** under the diagnostic prompt (run41); the runs-against
condition (mean < 2.25) fired. The loss is entirely on **B3, limitations in one place: 4/4 → 0/4**.
Reading the artefacts: every run41 artefact rebuilt §13 correctly but kept an operational-definition
scope sentence in the body ("the review is organised against one operational definition of clinical
reasoning"), which the case's gold definition counts as one of the four limitation statements; under
the standard prompt the same package moves it into §13. The behaviour is prompt-conditioned, not a
scorer artefact; a candidate pre-registered edit (scope statements that bound the review belong in
Limitations) is recorded for a future round, not shipped.

### Third subagent blind-review pair — headroom, and the competitor is preferred

Pair: package run33 `ours-a1` vs anti-defensive `anti-defensive-a2` (both v2 0.67; text similarity
79.1%, judge-visible headroom). Four fresh subagents, both orders × low/high deliberation:

| condition | agreed dims | flips | verdict on agreed dims |
|---|---|---|---|
| low | logic (package), flow/interest/overall (competitor) | 2/6 (33%) | **anti-defensive 3–1** |
| high | logic (package), flow/interest/pleasure/overall (competitor) | 1/6 (17%) | **anti-defensive 4–1** |

Low-vs-high agreement **4/4 (100%)** on co-resolved dimensions. Both conditions prefer the competitor
on flow, interest and overall and the package on logic (the package's hedged claims vs the competitor's
overclaims). Protocol rate after three pairs: headroom pairs resolved (2/2 — one package-favoured, one
competitor-favoured, so the protocol is not package-biased), near-identical pair unresolved (1/1). This
is a same-family second reader, not an anchor, and one pair is a direction, not a rate.

### Still open after round 6

- No ranking, effect size, or independent/human anchor; "comprehensive superiority" in the reader
  sense is not established — a competitor has been preferred on one judge-visible pair.
- The B3 mode-fragility has no decision yet: the candidate scope-statement edit is recorded for a
  future pre-registered round.

## Round 7 — the scope-statement edit repairs the diagnostic-prompt mode fragility (package 1.2.5)

Round 6 found the package mode-fragile on B3 (limitations in one place): standard prompt 3.000/3 on
the hard case, diagnostic prompt 1.750/3 with B3 0/4, traced to an operational-definition scope
sentence staying in §3 under the "full revision" instruction. Round 7 shipped one pre-registered edit
— \`core/reader-layer/\`: **a scope statement is a limitation** (a sentence that bounds what the work
covers belongs in Limitations; the body may carry a neutral pointer only) — and measured it in the
condition where the defect was found: 4 fresh package-1.2.5 artefacts, the diagnostic prompt
byte-identical to run40/run41, review scorer B1/B2/B3.

**Result: 1, 3, 3, 3 — mean 2.500/3**, B1 4/4, B2 3/4, **B3 3/4** (was 0/4). All four pre-registered
acceptance criteria passed (B3 ≥3/4; mean ≥1.75; B1 4/4; B2 ≥3/4) and the edit is kept. The residual
is one of four draws (ours-k1) that keeps the scope sentence in §3 and closes the introduction on an
answer-shaped sentence the B2 formula does not match — the package's current within-arm variance on
this case. Reference entries identical, no number removed, the scope sentences relocated (not
deleted). Descriptive comparisons: 15 wins, 1 tie, 0 losses in 16 cross-pairs against ARS's 0.250;
12 wins, 1 tie, 3 losses against the pre-edit package under the same prompt (the losses are the one
conservative draw).

**The package now ships 1.2.5.** Behaviour summary on the measured instruments: working case
standard-prompt v2 **1.00 ×4** (competitors 0.00–0.67); hard case standard prompt **3/3 ×4** (ARS
0.25); hard case diagnostic prompt (controlled) **2.500/3** vs ARS 0.250 with 15/16 cross-pairs.
Screens A/B align with the v2 properties 25/25 and 29/29. Every change since 1.1.0 was a
pre-registered, verified edit with a revert condition.

### The honest final bound

No ranking, no effect size, no independent or human anchor; two constructed cases, one model family.
The third subagent blind-review pair resolved in a competitor's favour on reader dimensions (gen78),
so "comprehensively surpass" is established on the pre-registered objective instruments (no
characterised competitor reaches these scores) and bounded on general reader preference. One of four
draws per batch is the package's current residual variance on the hard case.

## Reproducing

The research apparatus lives in this repo's `bench/` directory (case construction, arm runs, freeze
manifests, property-span metrics, review-genre scorer, dual-order judge, independent-family judge
client, reports). Every number above is a direction from frozen artefacts and, where judging is
involved, agreement-filtered dual-order judging; none is an effect size, and none was measured on a
sample of manuscripts large enough to generalise beyond the constructed cases named.