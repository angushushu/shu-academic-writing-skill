---
name: shu-academic-writing-skill
description: >-
  Develop, diagnose, revise, and audit an empirical research manuscript for a peer-reviewed
  venue. Use when planning or restructuring a paper; when an introduction, abstract, or
  discussion does not land; when prose is dense or overlong; when claims may outrun the
  design; or when preparing a pre-submission readiness check. Covers reader-value and
  argument structure (McEnerney), sentence-level clarity (Williams), evidence-provenance
  discipline, and venue-compliance auditing. Portable: no plugin system, no platform
  binding, stdlib-only scripts. Read `project/` for the facts of the specific manuscript
  before making any claim about its content.
---

# Scholarly Writing

A portable, self-contained method for taking an empirical manuscript from problem statement
to submission. Copy this directory into any writing project; nothing outside it is required.

## How to use this bundle

Every module is a plain Markdown file. **Invocation means reading the file.** There is no
plugin system, slash command, or registry. Paths below are relative to this directory.

Resolve this directory's location once (it is wherever `SKILL.md` and `core/` sit together),
then read modules by relative path.

## Two layers — the distinction that makes this reusable

| Layer | Contents | Edit? |
|---|---|---|
| `core/` | Generic method. Applies to any empirical manuscript in any field. | Never edit per project |
| `project/` | This manuscript's facts: file map, venue rules, verified numbers, term table. | **Always fill in before use** |

`core/` tells you *how* to think. `project/` tells you *what is true here*. Keeping them
separate is what lets you copy the bundle to a new paper without dragging the last paper's
terminology, sample sizes, and journal limits with it.

**Read `project/project-profile.md` first, every time.** If it still contains template
placeholders, say so and ask the author to fill it in rather than inventing project facts.

## Read the module before you judge

**This is the most-violated instruction in this bundle, and it is binding.**

Naming the module that fits a job is not doing the module. Knowing that an audit is what is
wanted will not tell you what an audit of *this* manuscript must examine, and the failures
that actually sink papers — a claim the Discussion reverses, an analysis the Introduction
promises and no section delivers — are not visible to general editorial judgment, however
confident that judgment feels.

So, before producing any finding, ranking, or revision plan:

1. Name the job. Usually one of: **audit** (adversarial gate, findings and severity),
   **argument** (does it matter to these readers), **develop** (plan, draft, restructure),
   **prose** (sentences only), **reviewers** (a decision letter arrived).
2. Open that module's `SKILL.md` and read it. If it names a reference file that bears on your
   job, read that too. The table below is an index; the files are the method.
3. Only then read the manuscript and work.

The cost of this is a few thousand words. What it buys is measured, and it is narrower than the
paragraph above implies: **a reviewer that reads the module fabricates far less.**

On a real 4,740-word manuscript with 24 verified defects, reviewers that did not read the module
quoted text that **does not appear anywhere in the manuscript** in 8 of 9 runs (mean 20% of their
quotations). Reviewers that read it did so in 3 of 10 (mean 4%). Two contract shapes, same
direction, Welch p ≈ 0.0008.

It does **not** buy more findings. The same runs show module-readers reporting *fewer* problems
(5.5 versus 9.4), and the difference in how many defects they located favours the non-readers at
0.62 versus 0.43 — though that comparison is under-powered and should not be treated as settled
either way. Any claim that this bundle helps you find more is not supported by its own benchmark.

Two exceptions, and only these: a single-sentence question about terminology, and a project
whose `worklog.md` shows the same module was already run in this session and its findings are
still on the table.

## Modules

The table says which file fits which job. Reading that file is not optional — see the
instruction directly above.

| Module | Read when | Do not use for |
|---|---|---|
| `core/problem-framing/SKILL.md` | Before drafting anything. Frame the paper as a problem in the reader's existing understanding -- name what they believe, show why it fails, make the reader's work small. | Polishing sentences; verifying evidence |
| `core/reader-layer/SKILL.md` | The paper is correct but hard to read, or before any writing pass. One argument, one stake, no interruptions; the most validated module in this bundle. | Checking numbers, adding disclosures, venue compliance |
| `core/develop-manuscript/SKILL.md` | Planning, drafting, restructuring, substantive revision. The orchestrator. | Isolated sentence polishing |
| `core/engineer-argument/SKILL.md` | The draft does not obviously matter to its readers. Contribution, problem, movement, intro/discussion logic. | Copyediting |
| `core/polish-prose/SKILL.md` | The argument is settled and the sentences are hard to read. | Repairing an unstable argument |
| `core/audit-manuscript/SKILL.md` | Adversarial pre-submission gate; reviewer simulation. | Drafting; resolving evidence conflicts in the author's favor |
| `core/respond-to-reviewers/SKILL.md` | A decision letter has arrived. Triage, response letter, revision plan. | The pre-submission audit — that is a different job |
| `core/corpus-metrics/SKILL.md` | A review needs to say whether a number is *unusual* for the venue. **Optional; heavy dependencies.** | Anything, if its `doctor` check fails |

## Order of operations

Work top-down. Each layer is wasted effort if the layer above it is broken.

1. **Problem framing and argument** — `core/problem-framing/` then `core/engineer-argument/`. Does the draft change anything for a specific community of readers, and is the reader's existing understanding named and destabilised? A paper an editor stops reading in paragraph two cannot be rescued by clean sentences. Does the draft change anything for a
   specific community of readers? A paper an editor stops reading in paragraph two cannot be
   rescued by clean sentences.
2. **Writing and evidence** — `core/reader-layer/` for the reader surface, then `core/develop-manuscript/` for structure, numbers and the length loop. Do the claims match what the
   design can establish? Is every number traceable?
3. **Sentences** — `core/polish-prose/`. Only once claims and structure are stable.
4. **Adversarial gate** — `core/audit-manuscript/`. Before declaring anything submission-ready.


Do not let prose polishing conceal an unresolved evidence or design problem. That is the
single most common way this workflow gets misused.

## Where the project is: the stage model

The order of operations above is the *revision* loop. It runs inside a longer lifecycle. Read
`project/worklog.md` first to find which stage the project is actually in — do not infer it
from whichever file the author happened to open.

| # | Stage | Done when | Work here |
|---|---|---|---|
| 0 | **Setup** | `project/project-profile.md` and `venue-target.md` are filled | Fill the project layer |
| 1 | **Problem and value** | The seven spine sentences exist and survive a hostile "so what?" | `engineer-argument`, `project/manuscript-blueprint.md` |
| 2 | **Evidence map** | Every planned claim points at a result, code path, or citation; gaps are marked as gaps | `develop-manuscript`, `project/evidence-ledger.md` |
| 3 | **Outline** | Section functions assigned; theory set minimal; budgets allocated | `develop-manuscript`, `project/theory-map.md` |
| 4 | **Drafting** | A complete draft exists, however rough | Author writes; modules diagnose on request |
| 5 | **Argument revision** | Value and movement hold under review; claims calibrated to design | `engineer-argument` |
| 6 | **Prose revision** | Sentences read cleanly; terminology consistent | `polish-prose` |
| 7 | **Pre-submission audit** | Verdict is `submission-ready on available evidence` | `audit-manuscript` |
| 8 | **Submission package** | Manuscript, statements, data, code, and cover letter all built and checked | `develop-manuscript/references/submission-package.md` |
| 9 | **Reviewer response** | Point-by-point response and revised manuscript sent | `core/respond-to-reviewers/SKILL.md` |
| 10 | **Final** | Accepted; proofs checked; repository links live and permanent | `submission-package.md` § *After acceptance* |

Stages 5–7 iterate, and stage 9 usually sends you back through 5–8. That loop is normal and is
not a sign of failure; treat a returning manuscript as a new pass, not as a patch job.

**Two rules about stages.** Do not do stage-6 work on a stage-5 problem — that is the misuse
warned about above. And do not let stage 7 be skipped because a deadline is close; the audit
exists precisely for the moment when skipping it is most tempting.

## Screening scripts

Stdlib-only Python 3, no third-party packages, cross-platform. They are deterministic
screens, not judgment. A clean run proves nothing; a flag is a prompt to look, not a verdict.

```bash
python scripts/intake_screen.py DRAFT.md --profile project/venue-target.md
python scripts/argument_screen.py DRAFT.md
python scripts/check_manuscript.py DRAFT.md --profile project/venue-target.md
python scripts/audit_draft.py DRAFT.md --patterns project/claim-risks.md
python scripts/prose_lint.py DRAFT.md
python scripts/textmetrics.py DRAFT.md
python scripts/worklog.py status
```

Use `python3` instead of `python` where that is the working interpreter name. Every script
runs with `--help`.

`argument_screen.py` is the one to run after the reader layer: it flags an abstract that carries
gap framing anywhere (or states no finding), an introduction whose closing sentence does not carry the
answer, and every qualification still sitting inside a Results claim. It is a screen, not a score.

## Standing rules

These hold across every module and override any local convenience.

- **Never invent provenance.** Citations, DOIs, coefficients, intervals, sample sizes,
  reliability figures, exclusions, preregistration, ethics approval, and repository links are
  either traceable to a source or they are not stated.
- **When sources disagree, report the conflict.** Do not silently pick the favorable number.
  Privilege re-runnable outputs over prose summaries.
- **Calibrate claims to design.** Associational language unless the design identifies a
  causal effect. See the calibration ladder in `core/polish-prose/references/style-guide.md`.
- **Preserve null, negative, and heterogeneous results.** A calibrated contribution is
  stronger than an inflated one.
- **Distinguish levels of analysis.** Participants are not observations; stimuli are not
  populations. Repeated measures are not independent sample size.
- **Author-led by default.** Diagnose, map, question, and checklist. Do not write or rewrite
  manuscript prose unless the author explicitly asks for drafted text. This default is
  restated in each module because it is the one most often violated.

## Attribution

`further-reading.md` records the sources these modules draw on — McEnerney, Williams, Bem, and
the Harvard psychology guide — and flags the one place where a classic source's advice should
not be followed as written. None of them is a citable source for a manuscript's own argument;
they are revision methods.
