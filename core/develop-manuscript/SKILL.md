---
name: develop-manuscript
description: >-
  Orchestrate evidence-grounded development of an empirical manuscript: planning, drafting,
  restructuring, substantive revision, integrating theory with methods and results,
  reconciling project artifacts, and preparing a submission-ready paper plus supplement. Use
  when the work spans the whole paper rather than one passage. Do not use for isolated
  sentence polishing or for an independent adversarial audit.
---

> **Where this module sits.** Part of the stage model in `SKILL.md`, mapped in
> `core/MODULE-MAP.md`. Before declaring any draft submission-ready, read
> `core/audit-manuscript/SKILL.md` — the adversarial gate every other module stops short of.

# Develop the Manuscript

The orchestrator. It sequences the other modules and holds the provenance discipline that
keeps a draft honest while it grows.

## Start from project truth, not memory

Read these before writing anything substantive. Paths are relative to the bundle root.

0. `project/worklog.md` — **read the state block first, every session.** It says which stage
   the project is in, what is open, and which decisions are already settled. Run
   `python scripts/worklog.py status` for the block plus a staleness check; if the check
   reports the block is stale, say so and confirm before relying on it.
1. `project/project-profile.md` — what this project is, where its artifacts live, which file
   is authoritative for what. Locate the relevant artifact without loading the whole repo.
2. `project/evidence-ledger.md` — read **before stating any numerical result, sample size,
   hypothesis outcome, or reliability claim.**
3. `project/venue-target.md` — before changing structure, length, transparency statements, or
   reporting style.
4. `project/manuscript-blueprint.md` — when planning or restructuring the full argument.
5. `project/theory-map.md` — when selecting, adding, or removing theoretical frameworks.
6. `references/section-functions.md` (in this module) — the generic job each section performs.

If a project file still holds template placeholders, stop and ask. Do not fill project facts
from inference.

## Work in passes

1. **Define the claim.** One sentence each: the problem, the proposed contribution, the
   empirical test, the result pattern, the boundary, the broad consequence. If any sentence
   is hard to write, the paper is not ready to draft.
2. **Audit claim–design alignment.** Classify every main claim as descriptive, associational,
   predictive, mechanistic, or causal. Downgrade the wording wherever the design cannot carry
   the stronger class. Do this before drafting, not after.
3. **Choose the smallest theory set.** One primary framework. Admit a second only when it
   performs a distinct argumentative job or generates a rival prediction. A catalogue
   introduction reads as uncertainty about the contribution.
4. **Build an evidence map.** Map each planned claim to a specific result, code path,
   reliability output, or citation. Mark unresolved items as unresolved. Never close a gap
   from memory.
5. **Draft for the outer reader.** Establish the general problem before any local machinery
   or terminology. Define each technical construct in plain language at first use.
6. **Separate confirmatory from exploratory.** State the actual chronology. Do not
   retroactively label an analysis preregistered or a hypothesis confirmatory.
7. **Calibrate the contribution.** Emphasize what the design can establish. Treat mechanism
   and unmeasured constructs as interpretation, and say so.
8. **Revise in order.** `core/engineer-argument/SKILL.md`, then `core/polish-prose/SKILL.md`.
   Never the reverse.
9. **Run the adversarial gate.** `core/audit-manuscript/SKILL.md` before calling a draft
   submission-ready.
10. **Write the baseline first, with `core/reader-layer/SKILL.md`.**

    That module carries the method and the measured case for it: one argument, one stake, no
    interruptions. Read it and use it for the draft. Do not audit while writing -- the audit is
    steps 11 to 13, and doing both at once is the single measured cause of unreadable output in
    this bundle.

    **The paper you would write with no method at all.**

    Write it as a competent author would, with no checklist in front of you. State the stake, the
    confound that makes the measure necessary, what was measured, what was found, the result that
    cuts against it, what it means. Move the reader from one sentence to the next. That draft is the
    baseline, and **the rest of this module exists to preserve it while repairing it**, not to
    replace it.

    This ordering is not a preference. Two rounds of blinded forced choice, six questions per pair,
    put this bundle's revisions at **4 wins to 32** against a plain unaided rewrite. The unaided
    versions read better because they were never specified -- and a specification is what the rest of
    this module had become. So write the baseline first, and treat everything below as surgery on a
    living text rather than a template to fill.

11. **Run the audit on the finished draft, and patch locally.**

    Measured: the same audit, applied to a paper that already reads, costs **8 forced choices of
    readability out of 24 (p = .15, not detectable) and buys +4.5 compliance items**. Applied
    while writing, it cost the paper entirely (6 wins to 42 against no method). **The audit is
    nearly free after the draft exists and ruinous during.** So run it here, on the file, after
    step 10, never earlier.

    Read `core/audit-manuscript/SKILL.md`, then patch locally. After the baseline exists, check it against a short
    list of objectively verifiable failures. Each has a **minimal patch**; none licenses a rewrite.

    | detector | test | minimal patch |
    |---|---|---|
    | number not in the record | grep the ledger for the figure | replace it with the ledger's value, or delete the number |
    | claim contradicts an adjacent table | read the claim against the numbers beside it | delete the claim, or narrow it to what the table shows |
    | citation with no reference entry | every author-year has an entry | add the entry, or drop the citation and rephrase |
    | promised analysis not reported | each promise in the Introduction has a result | report it in one sentence plus a row, or delete the promise |
    | marker or placeholder | `[RQ1]`, `(REF)`, `<Table N here>`, `[why this matters]` | delete it, or say the thing in words |
    | arithmetic does not reconcile | recompute every derived statistic | replace the one wrong number |
    | unhedged overclaim | causal verb on a correlational design | swap the verb: `demonstrates` -> `was associated with` |

    **The patch is local.** Replace a clause, a sentence, a number, a citation. Do not regenerate a
    paragraph to fix a number in it: regeneration is what destroys the baseline, and it is not needed
    for any item in the table. If a detector fires on more than a handful of places, the draft has one
    systematic problem -- fix the cause once, do not apply two hundred patches.

12. **Relocate, never qualify.** Anything that would add a caveat, a disclosure or a limitation to a
    body paragraph gets **moved** to one disclosure section near the end, not inserted where it
    interrupts the argument. Registration, ethics, AI use, data and code availability, sensitivity
    analyses, alternative explanations, multiple-comparison decisions: all of it lives there, in the
    order a reader would ask.

    A revision that spread its disclosures through the argument was described by blinded readers as
    "repetitive: the time confound is stated twice in consecutive intro paragraphs, the Discussion
    re-reports Results, the Limitation is a six-item audit list", and lost. The disclosures are
    necessary; their position decides whether the paper is readable. The test: cover the disclosure
    section and the paper still reads as a complete argument; uncover it and nothing in the body is a
    surprise.

13. **Close the loop on length, then gate.** This is a control step, not a proofread step.

    Report every analysis, and frame every deviation as what it establishes -- the register that won
    logic 4-0 against the comparison skill. Followed open-loop, that instruction doubled the paper and
    lost flow 1-3: 9,100 words against a ~2,500-word budget for Method and Results, and the judges'
    words were that it buried the argument under provenance.

    So length is a **controlled variable and the loop must be closed on it**:

    ```bash
    python scripts/check_manuscript.py REVISED.md --profile project/venue-target.md
    ```

    1. Read the reported length for Method + Results. Over the venue's budget means not finished.
    2. Compress by **moving analyses, never by deleting them**: a table into a supplement, a
       sensitivity check into one sentence plus a pointer, a robustness arm into a footnote. A record
       surface pointing at a supplement that exists is legitimate; pointing at an analysis the paper
       does not contain is not -- that version lost 10-14.
    3. **Keep the register through compression.** "The window change removes the back-filled inflation;
       both estimates are in the supplement" is one clause and keeps the logic. Do not revert to "the
       window was changed after registration" to save words: that register lost logic 0-4 every time.
    4. Re-run the checker and re-read the length. Repeat until under budget, then run
       `scripts/intake_screen.py` and fix what it reports.

    The loop terminates when the length is within budget **and** every reported deviation still carries
    what it establishes. If compression would force you to drop a deviation's reason, cut an analysis
    from the main text instead and keep the reason.

## What a delivered manuscript may not contain

Each of these was observed in a delivered revision and cost it points. Check for them by search,
not by memory.

- **Internal markers anywhere, headings included.** `[RQ1]`, `[H2]`, `[exploratory]`, `[[…]]`,
  `(REF)`, `<Table N here>`, `TODO`. A heading is read by readers, not by you. Say the research
  question in words, or drop it.
- **An analysis named but not reported.** If you disclose a check, give its result, or state
  plainly that it cannot be reported and why. Naming an analysis and withholding its outcome reads
  as concealment and is worse than silence.
- **A record status upgraded into a claim.** If the authors' records leave something unresolved —
  what a registration covered, whether an approval exists, which window is primary — write that it
  is unresolved. Do not write that the registration "specifies" a detail the record does not
  settle.
- **A limitations section that omits non-independence.** When participants contribute many
  observations, serial dependence belongs in the limitations, not only in the analysis note.
- **A named work with no reference entry.** Every author–year in the text needs an entry, and so
  does every work named as a work: a film named with its year is a citation. A reference list that
  is short because you deleted the entry rather than the claim is not repaired.
- **An assertion about units you excluded.** Do not write that excluded recordings "do not differ"
  from the analysed sample unless the record contains that comparison. Absence of evidence is not
  the finding you want here; the finding is that they were excluded and why.
- **An analysis you describe but cannot quantify.** If the records do not let you report an
  estimate, remove the analysis or mark it explicitly as unreportable. A qualitative sentence —
  "a normalization check suggested the effect was not driven by scale" — is neither a result nor an
  omission, and a reviewer reads it as evasion.
- **A promised analysis deleted because the only numbers are inconvenient.** If the record has the
  figures under a different window, sample, or rule than the primary analysis, report them **and say
  which window they come from**. Deleting the question reads as concealment; reporting both and
  naming the mismatch reads as competence. This was the single largest scoring difference between
  two revisions of the same manuscript produced by the same method.
- **A primary analysis that silently departs from the registered one.** Report the registered
  estimate alongside the primary one, name which is which, and give the reason for the change. A
  reader who discovers the switch unaided will not believe the rest of the numbers.

## Preserve provenance

Read `references/provenance-rules.md` for the full discipline. The short form:

- Never invent citations, DOIs, coefficients, intervals, sample sizes, coder agreement,
  exclusions, preregistration, ethics approval, or open-science links.
- When artifacts disagree, report the conflict and privilege re-runnable outputs over prose
  summaries. Never silently select the more favorable result.
- Keep raw data and original coder records unchanged. Derived outputs go in clearly named new
  files that record command, environment, and inputs.
- Treat a small purposive stimulus sample as a boundary, not a footnote.
- Treat repeated within-participant observations as nested and autocorrelated. Do not present
  row counts as sample size or as evidence of precision.

## Author-led by default

Unless the author explicitly asks for drafted or rewritten prose, do not write manuscript
text for them and do not edit their draft file. Provide diagnoses, paragraph functions,
argument maps, questions, alternatives, and revision checklists that let the author write.

## Deliver revision work transparently

For substantive edits, report:

1. the revised text or artifact;
2. a change log organized by argument, evidence, and style;
3. an unresolved-evidence list;
4. current venue-compliance status;
5. commands and checks run, with their results.

**Then land it.** A handoff that exists only in a chat transcript is lost the moment the
session ends — and the author may be in a different tool tomorrow. Append the durable part to
`project/worklog.md` and refresh its state block:

```bash
python scripts/worklog.py add
```

Keep the entry to a few lines. What belongs there is what would otherwise be re-derived: the
stage, what changed, what was decided, what is still open, and any AI assistance the venue
will require you to disclose. Detail belongs in the artifacts it describes — verified numbers
in `project/evidence-ledger.md`, claim wording in `project/claim-risks.md`. A decision that
should not be reopened goes in the worklog's standing-decisions table.

Run `python scripts/check_manuscript.py DRAFT.md --profile project/venue-target.md` as a
screening report. It is a deterministic preflight, not editorial judgment.

For stage 8, work from `references/submission-package.md`.

## Revision rounds

A revision is usually more than one pass. Two shapes are supported, and the guardrails below are
measured, not stylistic.

**One round** is always the same order: reader layer -> the scripts -> the audit -> fix objective
defects. Never the audit first, and never the two interleaved. Record the round in
`project/worklog.md` (`python scripts/worklog.py`) with what it fixed and what it did not.

### Unsupervised rounds — the model iterates on its own

Permitted, up to **three rounds**, and under three rules that each come from a measured failure:

1. **Never delete a correction.** A later round must not remove an analysis, a disclosure or a
   qualification that an earlier round added. Measured: a round asked to make an already-audited paper
   read better deleted two reported analyses, and the pair went from 16-8 in favour to 8-16 against,
   with mechanical compliance dropping from 9/12 to 7/12. If a round has removed content, it failed;
   revert it.
2. **A round is progress only when it resolves a checker finding or a named reader defect.** A round
   that reorganises without either is motion, and three rounds of motion is how a paper acquires the
   seams that the next reader notices. The stopping rule is: no new finding from
   `check_manuscript.py` / `intake_screen.py`, length within budget, and no question from
   `core/reader-layer/` still unanswered.
3. **Stop at the first round that adds no finding and removes nothing.** Further rounds at that point
   have been observed only to make things worse.

### Supervised rounds — a human is in the loop

Two shapes, and the second is safer:

- **approve each diff.** You propose one change at a time with its reason; the human accepts or
  rejects. Good when the changes are few and consequential.
- **suggest, then apply.** You report what you would change and why; the human edits the file. Good
  when the human knows the material better than you do.

In both, the human's job is not to write the revision. It is **to reject the plausible-looking edit**.
Every measured regression in this module's history read as an improvement at the time it was proposed,
which is why the proposal needs an independent eye rather than a stronger argument.

Record each accepted and rejected suggestion in the worklog, so a later round does not re-propose what
was already declined. A rejected suggestion without a recorded reason will come back.

### Do not loop on prose

If two rounds have both ended in sentence-level rewriting, the problem is an unsettled argument, not
unfinished sentences. Go back to `core/engineer-argument/` rather than running a third polishing round.
