# Changelog

## Repository (docs only, 2026-10-22)

- Published as a standalone repository: github.com/angushushu/shu-academic-writing-skill.
- `README.md` rewritten as a bilingual (English/中文) quick-start; the benchmark results and the
  version-by-version evolution now live in `BENCHMARK.md`; `EVIDENCE.md` remains the full measurement
  record.
- License aligned with the repository: GPL-3.0.

## 1.2.5

Candidate edit, **pre-registered before measurement** (`bench/PRE-REGISTRATION-ROUND7.md` §W1);
acceptance rule fixed in advance. Do not cite as measured until the run42 result paragraph is appended.

- `core/reader-layer/`: a **scope statement is a limitation**. A sentence that bounds what the work
  covers (the operational definition it is organised against, the selection procedure, the source set)
  belongs in Limitations, not in the argument; the body may carry a neutral pointer only. Reason
  (measured, gen78): under the "full argument revision" instruction the package's hard-case artefacts
  rebuilt §13 but kept the operational-definition scope sentence in §3 — B3 (limitations in one place)
  fell 4/4 → 0/4 relative to the standard prompt, with the total 3.000 → 1.750. One behaviour change;
  no script change.

**Measured result (run42, four fresh artefacts, diagnostic prompt, pre-registered acceptance rule, all
four criteria passed).** Kept: B3 **3/4** (was 0/4), mean **2.500/3** (was 1.750), B1 4/4, B2 3/4. The
mode fragility is largely repaired in the condition where it was found; one of four draws (ours-k1)
still keeps the operational-definition sentence in §3 and misses the B2 formula, which is the package's
current within-arm residual on this case. Reference entries identical, no number removed; the scope
sentence was relocated, not deleted. Version 1.2.5 is the behaviour this bundle ships.

## 1.2.4

Candidate edit, **pre-registered before measurement** (`bench/PRE-REGISTRATION-ROUND4.md` §W1);
acceptance rule fixed in advance. Do not cite as measured until the run38 result paragraph is
appended.

- `core/reader-layer/`: the introduction's last paragraph must **close on** the answering sentence.
  If the paragraph states the finding and then hands off to the evidence, repeat the answer as the
  closing sentence (or move it last). The two-minute test and the run-screen text say so. Reason
  (measured, gen73): the post-A1-edit batch put the answer inside the closing paragraph and ended on
  evidence — A2 final-sentence 0/4, v1 below its guide.
- `scripts/argument_screen.py`: screen B now checks the introduction's **closing sentence** (was: any
  answer language in the closing paragraph). Instrument validation before any run: on 29 frozen
  empirical-case manuscripts the rule agrees with property-span v2 A2 = 1.0 on **29/29** (the
  paragraph rule: 21/29); the clean reference passes and the damaged draft fails. Reproduce:
  `python bench/check_screen_b_alignment.py`.

**Measured result (run38, four fresh artefacts, pre-registered acceptance rule, all four primary
criteria passed).** Kept: A2 closing-sentence pass **4/4** (was 0/4), property-span v2 **1.00 ×4**
(mean 1.000, was 0.833), tightened screen **4/4 exit 0**, A1 still 4/4, v1 **0.723** (was 0.550;
pre-edit run33 was 0.732). The working-case metric is now at its ceiling for this package (four draws
all at 1.00), so it becomes a regression test rather than an improvement instrument: further package
work must be measured on the hard case or a new case. Full numbers and the negative blind-review
replication from the same round are in the research repo's gen76 report.

## 1.2.3

Candidate edit, **pre-registered before measurement** (`bench/PRE-REGISTRATION-ROUND3.md` §W2);
the acceptance rule and the revert condition were fixed in advance and are not tuned here. Do not
cite this entry as a measured improvement until the run37 result paragraph is appended.

- `core/reader-layer/`: gap framing is not allowed anywhere in the abstract. A
  "the literature has not ..." sentence belongs in Related Work or the introduction's first
  paragraph even when a stake or a finding precedes it; the two-minute test and the screen
  section say so. Reason (measured, run33): 2 of 4 package artefacts left exactly such a
  sentence in the abstract after the opening while passing the old screen (v2 A1 = 0.00).
- `scripts/argument_screen.py`: screen A now checks the **whole abstract** -- any gap-framing
  formula, or no finding-language marker, flags it. Instrument validation before any run:
  on 25 frozen empirical-case manuscripts the rule agrees with the v2 A1 property **25/25**
  (the opening-only rule agreed 20/25); the clean reference exits 0 and the damaged draft
  exits 1 with all three flags. Reproduce: `python bench/check_screen_a_alignment.py`.

**Measured result (run37, four fresh artefacts, pre-registered acceptance rule).** The A1 defect is
repaired: **A1 4/4** (from 2/4 in the pre-edit batch), every abstract states the finding and carries
no gap framing, and the gap claim survives in the introduction's first paragraph. property-span v2
**0.833 ×4** (mean 0.833, baseline 0.792); tightened screen **4/4 exit 0**; A4 at the clean
reference's level 4/4. Two honest caveats are recorded with the result: the pre-registered A4
"pass count" was mis-specified (its raw threshold fails the clean reference; the intent reading,
A4 span = 1.00 on 4/4, is what is claimed — full adjudication in the research repo's gen73 report),
and A2 moved from the closing *sentence* (3/4 before) to inside the closing *paragraph* (0/4 final
sentence, 4/4 closing paragraph), which lowered the secondary v1 metric (0.550 vs the 0.60 guide).
The edit is kept because its target — abstract-wide gap framing — is verifiably fixed at no v2 or
screen cost; the A2 clarification is a candidate for one future round, not this one.

## 1.2.2

Evidence-only release; no package behaviour changed.

- `README.md` / `EVIDENCE.md` now report the multi-artefact distributions instead of single scores:
  four fresh runs of the package on the constructed case give property-span v2 1.00 / 0.83 / 0.67 /
  0.67 (mean 0.79) and pass the deterministic screen 4/4; the same round shows one artefact is not an
  estimate and that the same competitor skill can be applied in a mode that repairs nothing measured —
  so no ranking against ARS is claimed.
- A harder second constructed case (different genre and source; damage touching 78% of prose paragraphs)
  is now usable — median cross-arm similarity 80.4% — with a pre-registered review-genre scorer on
  which the package scores 4/6 vs ARS 1/6 (n=2).
- The independent-judge attempt is documented, including its failure mode: frontier Gemini unavailable;
  a local 7.5B independent-family judge was 75% order-dependent and cannot serve as an anchor. That
  pilot is **retired**; the next protocol is a same-family subagent low/high blind review, with human
  raters or a frontier model as the stronger anchor (research repo: `bench/JUDGING-PROTOCOL.md`). The
  question stays open.
- New in the research repo (not shipped in the bundle): `bench/gemini_judge.py`, the review-genre
  scorer, the hard case and their reports (gen67–gen70).

## 1.2.1

Screen C of `scripts/argument_screen.py` now separates a **limitation** stated inside Results (a
flag: it belongs in Limitations) from a **claim calibration** ("we do not claim …", "should be read
with …", kept as a note). Measured reason: on the constructed case the clean reference keeps one
calibration sentence in Results and the damaged draft also carries a limitation sentence there; the
first version of the screen printed both as "informational", so a run that passed the first two
screens treated the draft as finished and left the limitation in place. Validation on the case's
known artefacts: clean reference exit 0 (one calibration note), damaged draft exit 1 (three flags),
ARS exit 0, run24 package arm exit 1 (introduction close), a second package run exit 1 (limitation
in Results). `core/reader-layer/` updated to say that a printed limitation is work to do while a
calibration note may stay.

The 1.2.1 test run on the constructed argument-damage case restored all three planted argument
surfaces: property-span v2 **1.00**, screen **exit 0**. A blinded dual-order judge on that artefact
preferred it to ARS 5–1 and to nature-skills 6–0 (0% order-dependent dimensions on both pairs),
was undecided 3–3 against PaperSpine, and did not establish an order against anti-defensive (50%
order-dependent). `README.md` and `EVIDENCE.md` now carry the constructed-case evidence (packages and
baselines compared, the version trajectory, the second case's negative result, the judge cross-check,
and the instrument errors that led to v2 and to this screen). No behaviour changed between the 1.2.1
code and these docs.

## 1.2.0

The check that makes the writing pass verifiable, and two docs fixes.

- **New script `scripts/argument_screen.py`** (stdlib-only): deterministic screen for the three
  argument-surface defects the constructed case exposed — an abstract that opens on gap framing, an
  introduction whose last paragraph does not carry the answer, and every qualification sitting inside
  a Results claim (printed for a manual read, never auto-failed). Validated on the case's known
  artefacts: the clean reference and the comparison package pass; the damaged draft fails two
  screens; two runs of this bundle each fail exactly the screen corresponding to what each missed.
- `core/reader-layer/`: "Run the screen before delivery" section — run it, resolve every flag by
  moving the answering sentence or the qualification (never soften or delete), run it again.
- `SKILL.md` and `README.md` script lists now name all seven scripts; script counts reconciled.
- Cosmetic: escaped quotes (`\"`) removed from the reader-layer Markdown; no instruction changed.

## 1.1.0

One verified edit, from the constructed argument-damage case.

- `core/reader-layer/`: new move 2 — **put the answer where the reader looks for it**. The abstract and
  the last paragraph of the introduction must each state what the paper establishes. Measured on the
  constructed case: the previous version repaired six argument damages but left the paper's answering
  sentence in the Discussion (property-span P2 = 0.00, introduction ends on a results preview); the
  clean reference and the comparison package both close the introduction on that sentence. The
  two-minute test gains the matching check.
- No other module changes. The two-pass architecture and the audit boundary are untouched.

## 1.0.0

First public release.

- Two-pass architecture: `core/reader-layer/` writes the argument, `core/audit-manuscript/` corrects
  the finished file. The order is the product; an earlier version that merged them scored 6–42 against
  an unaided rewrite.
- `core/problem-framing/` added: frame the paper as a problem in the reader's existing understanding.
  Measured neutral on judged quality, positive on mechanical compliance.
- Length loop in `core/develop-manuscript/` step 13: compress by moving analyses into a supplement, keep
  each deviation's reason intact. Without it, reporting everything doubled the paper and lost flow.
- Six stdlib-only scripts for intake, venue limits, claim risks, section word counts and the worklog.
- `EVIDENCE.md`: every measurement, every overturned claim, and all sixteen instrument errors.