---
name: respond-to-reviewers
description: >-
  Triage a decision letter and build a point-by-point response and revision plan. Use when
  reviews have come back — major or minor revision, reject-and-resubmit, or a rejection worth
  appealing — and the author must decide what to concede, what to contest, and in what order
  to revise. Covers reading the editor's letter for what it actually asks, separating
  reviewer requests by cost and merit, response-letter structure, and the rhetoric of
  disagreeing without antagonizing. Do not use for the pre-submission audit; that is
  `core/audit-manuscript/SKILL.md`.
---

> **Where this module sits.** Part of the stage model in `SKILL.md`, mapped in
> `core/MODULE-MAP.md`. Before declaring any draft submission-ready, read
> `core/audit-manuscript/SKILL.md` — the adversarial gate every other module stops short of.

# Respond to Reviewers

A revision is not a patch job. The manuscript goes back through the same revision loop
(stages 5–8 in `SKILL.md`), and the response letter is a separate document with its own
readers and its own argument.

## Read the editor first, and read them literally

The reviews are input. **The editor's letter is the instruction.** Editors routinely signal
which reviewer concerns they consider binding and which they do not, and authors routinely
miss it because they read the reviews first and arrive at the editor's letter already
defensive.

Before planning anything, extract:

- The decision category, in the venue's own vocabulary, and what it commits the editor to.
- Which specific concerns the editor names in their own voice. These are non-negotiable.
- Which concerns the editor attributes but does not endorse. These are arguable.
- Any explicit constraint: length, deadline, additional analyses, a named statistical review.

If the editor's letter and a reviewer disagree, the editor wins. Say so in the response, in a
sentence, without gloating.

## Triage every point before answering any

Build the table before writing a word of the letter. Extract every distinguishable request —
including the ones buried mid-paragraph, which are the ones most often missed.

| # | Reviewer | Request (paraphrased) | Type | Merit | Cost | Response |
|---|---|---|---|---|---|---|

**Type:** evidence · analysis · framing · clarity · scope · citation · format.

**Merit — judge this before cost, and judge it honestly:**

- *Right* — the reviewer has found a real problem. Concede fully and fix it. Most points.
- *Right about the symptom, wrong about the cause* — the confusion is real, the proposed fix
  is not. Fix the confusion your way, and say what you did instead and why.
- *Wrong, and consequential* — must be contested with evidence. Rare. Budget for it.
- *Wrong, and inconsequential* — do it anyway if cheap. Contesting cheap points spends
  credibility you will need for the expensive one.
- *Out of scope* — a request for a different paper. Decline explicitly, name the boundary.

**Cost:** hours, plus whether it requires new data, a rerun, or a coauthor decision.

The triage table is a project artifact. Put it in the response letter's planning file, not in
your head, and record the merit judgments in `project/worklog.md` under standing decisions —
future-you will not remember why point 14 was declined.

## Revise before you write the letter

Authors write the letter first because it feels like progress. It produces promises the
revision then has to keep. Do the revision, then describe what you did.

Run the manuscript back through the loop: `core/engineer-argument/` if framing changed,
`core/develop-manuscript/` if claims or evidence changed, `core/polish-prose/` last,
`core/audit-manuscript/` before resubmitting. A revision that fixes fourteen local points and
breaks the argument's spine is a worse manuscript with a better response letter.

## Response letter structure

Two readers, and they read differently. The editor skims for whether you complied and whether
the paper improved. The reviewer looks for their own points and whether they were taken
seriously.

```markdown
[Opening: 3-5 sentences]
Thank the editor and reviewers without ceremony. State the two or three most substantial
changes. State plainly if any point was not adopted, so the editor is not surprised later.

## Reviewer 1

> [Quoted comment, verbatim and complete]

**Response.** [What you concluded.]
**Change.** [What you changed, and where — section, page, or line.]

> [Next comment]
...
```

Non-negotiables of the form:

- **Quote every comment verbatim.** Paraphrasing reads as evasion, even when it is not.
- **Answer every point.** Silence on a point reads as refusal. A one-line "changed as
  suggested, p. 7" is a complete answer for a minor point.
- **Point at the change.** Every response names where in the manuscript to look. A response
  that describes a change without locating it forces the reviewer to search, and they will
  conclude you did not make it.
- **Separate the conclusion from the edit.** What you decided, then what you did. Reviewers
  checking compliance need the second; editors weighing judgment need the first.

## Disagreeing well

You are allowed to disagree. Papers are weakened by authors who capitulate on everything —
including on points where the reviewer misread the design.

The move that works:

1. **Name what the reviewer got right first**, and mean it. There is almost always something —
   at minimum, that the passage was unclear enough to permit their reading.
2. **State the disagreement as evidence, not as position.** "The analysis in Table 3 addresses
   this because…" beats "we respectfully disagree."
3. **Concede the residue.** If their concern is 20% right, grant the 20% explicitly.
4. **Change something.** Even when you win the point, the fact that a trained reader reached
   that reading is itself evidence of a clarity problem. Fix that, and say you did.

What fails: "we respectfully disagree" with nothing after it; re-explaining the original text
more loudly; correcting the reviewer's competence; deferring everything to a limitations
paragraph; and silent non-compliance, which is the fastest route to a second rejection.

## Calibration still applies

Everything in `project/lexicon.md` and `project/claim-risks.md` governs the response letter
too. Under revision pressure it is tempting to promise more than the data support, or to
accept a reviewer's stronger causal phrasing because they suggested it. A reviewer asking you
to overclaim is a reviewer to be politely resisted — with the design-based reason stated.

If a requested analysis is run, its result enters `project/evidence-ledger.md` under the same
status vocabulary as everything else, and is reported whichever way it comes out. A revision
is not exempt from the provenance rules; it is where they are most often quietly broken.

## Output

1. The triage table, with merit and cost per point.
2. A revision plan ordered by dependency — argument-level changes before local ones.
3. The response letter.
4. A list of points declined, each with the reason given to the editor.
5. Anything requiring a coauthor decision or new data collection, flagged separately.
