---
name: reader-layer
description: >-
  Make a manuscript a reader wants to read: one argument, one stake, no interruptions. Use when a
  draft is correct but unreadable, when a reviewer says it is dense or hard to follow, or as the
  first pass before any audit. Do not use it to check numbers, disclose limitations, or verify
  venue compliance -- that is core/audit-manuscript/SKILL.md, and doing both at once produces a
  document instead of an argument.
---

# The reader layer

One job: make the paper an argument a person finishes. Nothing here checks a number, requires a
disclosure, or enforces a venue rule. Adding those while writing is what turns a paper into a report,
and it was measured: a version of this bundle that carried the compliance rules scored **6 wins to
42** against an unaided rewrite, while this layer alone scores **29 wins to 7** against the
comparison skill and **19 to 5** against no method at all, on blinded forced choices over logic,
flow, interest, comprehension, pleasure and overall.

Sequence matters. Use this layer first, then core/audit-manuscript/SKILL.md on the result.

## The one thing that decides it

A paper is read as **one argument**. The moment it becomes a set of analyses, the reader stops. Every
rule below exists to keep it an argument.

## Eight moves

1. **Open on a stake, not a gap.** "The literature has not formalised X" tells the reader nothing.
   "Anyone claiming these responses track character standing cannot test that claim at the timescale
   at which it is made" tells them what is at risk. A stake is a problem a person has; a gap is a hole
   in a bibliography.

   The abstract is not exempt. A gap sentence anywhere in the abstract -- after the opening, after a
   stake, after the finding -- is still a gap sentence: it tells a scanning reader what nobody has
   done instead of what is now known. Move it to Related Work or to the introduction's first
   paragraph, where a gap has a job (establishing the niche); do not leave it in the abstract because
   a stake precedes it. The screen below checks the whole abstract, not only its opening.

2. **Put the answer where the reader looks for it.** Before reading the body, a reader reads the
   abstract and the last paragraph of the introduction, and decides from those whether the paper is
   for them. Both must state what the paper establishes, in a sentence the reader could repeat
   afterwards. A results preview is not that sentence: "we find X in Study 1 and Y in Study 2" tells
   them what you did; "in neither setting does the score mean what its size suggests" tells them what
   is now known. If the only sentence carrying the paper's answer sits in the Discussion, the
   contribution is in the one place a screening reader never reaches. This is a placement rule, not a
   second draft: move the answering sentence to where readers look, and leave the evidence to earn it
   in the body. An abstract that opens on a stake but still carries a "the literature has not ..."
   sentence further down has hidden the answer just as effectively; the screen checks all of it.

   Close on the answer, not merely near it. If the paragraph states the finding and then hands off to
   the evidence, the last sentence a reader takes from the introduction is a result detail, not the
   finding. End the paragraph on the answering sentence, or repeat the answer as its closing sentence.
   The screen checks the last sentence, not just the last paragraph.

3. **One sentence carries one paragraph.** The first sentence states the point; the rest earns it. If
   a paragraph has two points, split it. If its first sentence is background, delete it.

4. **Never interrupt a case to be careful.** A qualification inside the paragraph making the claim
   reads as doubt about that claim. Move the qualification to where the reader expects it -- the
   limitations -- and let the argument run. Correctness is not served by hedging in the middle of a
   sentence; it is served by being right and then saying so.

   **A scope statement is a limitation.** A sentence that bounds what the work covers -- the
   operational definition it is organised against, the selection procedure, the source set, the
   knowledge it does not claim -- belongs in the Limitations section, not in the argument. If the body
   needs a pointer, make it a neutral one ("the scope defined in Limitations") and keep the bounding
   sentence itself in Limitations; do not leave the bound in the body and also mention it in passing.
   A limitation stated where the case is made is still a limitation stated where the case is made.

5. **Say each thing once.** An introduction that states the same problem twice, a discussion that
   re-reports the results, a limitation list that repeats the caveats already made -- all of it reads
   as padding and costs the reader's trust. Each section has one job; do it once.

6. **Let the awkward result do work.** The result that cuts against the story is the most interesting
   thing in the paper. Say it plainly, early, and use it. A paper that hides its counterexample reads
   as advocacy; one that leads with it reads as inquiry.

7. **Transitions carry weight.** A sentence at a section boundary should say why the next thing
   follows, not announce that it follows. "The next section shows" is a signpost; "If the measure is
   real, the films should not all behave alike" is a reason to keep reading.

8. **Close on the class, not the study.** "We found X in three films" is a summary and readers skip
   it. "Measures of this kind are worth testing against the clock they resemble, and diverge from it
   exactly where they can tell us something" is what they carry away.

## The two-minute test

Read the first paragraph and the last paragraph aloud. If the first does not make you want to know
what happened, rewrite it. If the last only restates what you found, rewrite it to say what it means
for anyone who will build the next one.

Then read the abstract and the final paragraph of the introduction. From those two places alone you
should be able to say what the paper establishes and why it matters. If the answer only appears once
you reach the Discussion, the paper has hidden its contribution: move the answering sentence to the
abstract and to the introduction's close. If either place needs a sentence about what the literature
has not done in order to make sense, that sentence belongs in Related Work; the abstract and the
introduction's close are for what is now known. Then read the last sentence of the introduction on its
own: it should be the answer, not a result or a plan for the next section. If it is not, move the
answering sentence to the end of that paragraph or repeat it there.

Then read only the first sentence of every paragraph, in order. Those sentences should be the argument
on its own. If they are not, the paragraphs are doing the wrong work.

## Run the screen before delivery

The two surfaces this layer is responsible for have a deterministic check:

```bash
python scripts/argument_screen.py DRAFT.md
```

It flags three things: an abstract that carries gap framing anywhere -- or that states no finding at
all -- an introduction whose closing sentence does not carry the answer, and any limitation stated
inside a Results claim. Claim calibrations
("we do not claim that ...", "should be read with ...") are listed as notes, not flags, because a
paper may legitimately calibrate a claim where the claim is made. Resolve each flag by **moving** the
answering sentence or the limitation to where it belongs -- do not soften the claim and do not delete
a correction -- then run it again. A limitation the screen printed is work to do: move it to
Limitations. A draft that ignores the sentences the screen printed is not a finished pass. A flag is
a prompt to read the printed sentence, not a verdict, and a clean run is not a passing argument
review. The screen checks placement, not quality: it cannot tell you whether the sentence is any
good.

The arm-level evidence for why this check exists: on a constructed argument-damage case, two runs of
this bundle each repaired six of the damaged sites but one missed the answer placement and the other
missed an interleaved limitation -- failures a two-second screen catches. The screen's vocabularies
are small on purpose; a re-worded answer can still be missed, and the flagged sentence is always
printed so a false alarm costs one read.

## After an audit, stop and check nothing was deleted

An audit inserts corrections in place, and they are what makes an audited paper fail to read. The
obvious move is to re-read and integrate them. **Measured, that move destroys the paper: the
reader+audit version scores 16-8 against the comparison skill and the same version after an
integration pass scores 8-16, losing logic 0-4 and overall 0-4, with two of the five compliance
checks newly failing.**

Asked to make an audited paper read better, an author resolves "this inserted block interrupts the
argument" by deleting the block -- which is the right response to the instruction and the wrong
thing for the paper, because the block was a correction. If you do re-read an audited draft, the one
thing that matters is what you must NOT do: **delete no correction to make a paragraph flow.** Reword
around it, move it to the section the venue expects, or leave the paragraph slightly heavier. A
correct paper that reads well is the goal; a well-flowing paper that dropped its analyses is not.

## Two surfaces, and what belongs on each

A paper has two audiences and they want opposite things. The **reader** wants one argument and never
looks at a compliance statement. The **editor and reviewer** want to verify: registration and its
coverage, ethics, AI use, data and code, sensitivity analyses, venue limits.

Give them different surfaces, and keep the boundary strict:

- **Reader surface** -- Introduction, Results, Discussion. One argument, no disclosures, no
  robustness material, no caveats interrupting a claim.
- **Record surface** -- the transparency statement, limitations, data and code availability. Status,
  location, and deviations: what was registered, when, what changed and why, where the materials are.

  **A pointer is not a disclosure.** A thin record surface that says "the registered estimates are
  reported in Results" is worse than one that carries them, unless Results really does carry them --
  measured, a pointer-thin version lost 10-14 to the comparison skill where a verbose one tied 12-12,
  and the reviewers named the reason: "listed among analyses not reported here. Promised step, never
  shown." Whatever the record surface points at must exist in the paper, reported. Thin is only
  available to a paper that is complete.

That last constraint is measured. A transparency statement that recites results before the reader
knows how the measure works is read as a document that has not decided which sections it is in:
reviewers described one as dumping "~3,600 characters of results before the reader knows how the
measure is computed", and it cost logic 0-4 and comprehension 0-4 against the comparison skill, leaving
the two at 12-12 overall despite the argument being better.

Numbers belong in Results, where they can be tied to a claim. The record surface says what happened to
the analysis, not what the analysis found.

## Disclosure, written as what it establishes

The register of a disclosure decides whether a reviewer reads competence or doubt, and it was
measured. Four attempts stated deviations as process facts -- "the window was changed after
registration", "a rule was tightened after an initial run" -- and every one lost logic to the
comparison skill (0-4, 0-4, 3-1, 0-4). Stating the same deviations as what they establish reversed it
to **4-0 on logic and 4-0 on overall**, and the version was preferred 9-3 by a reviewer.

The difference:

- **Process fact:** "The analysis window was changed after registration from the full series to the
  post-dialogue segment."
- **What it establishes:** "The registered analysis paired a back-filled constant with ratings still at
  rest, so it inflates the coefficient. Restricting to the post-dialogue segment removes that
  inflation; both estimates are reported, and the inflation is the difference between them."

Three rules:

1. **Never state a deviation alone.** Pair it with the distortion it removed, or with what the
   alternative would have produced. You have the reason; the reason belongs on the page.
2. **A null is a result.** Say what it rules out. "Under the stricter rule the pooled effect is null,
   which bounds the claim to the by-film reversals" is a finding; "the stricter rule was null" is a
   confession.
3. **Report it, then point to it.** A record surface that points at an analysis the paper does not
   contain is a promise, and a promise costs more than an omission (measured: 10-14).

The cost of this register is length: the version that won logic 4-0 was twice the venue's budget and
lost flow 1-3 for it. Say it once, compactly, and make the compression carry the argument rather than
the numbers.

## The three defects judges keep finding

Measured across eight end-to-end artifacts, these recur and each costs a dimension. Check for them by
search before you deliver.

1. **A phantom analysis.** The Discussion refers to a comparison that Results never reports -- "the
   normalised measure was statistically indistinguishable from a min-max rescaling", when no min-max
   arm appears in Method or Results. The claim is unfalsifiable as written and a reviewer reads it as
   invented. If it is not in Results, it does not exist.
2. **A group-mean table cited for a participant-level claim.** "The association was weakest in Rio
   throughout (Table 1)" where Table 1 holds curve-alignment means, not correlations. State the level
   of every table once, in its note, and never let a claim cross levels without saying so.
3. **Numbers from two windows in one paragraph.** A sentence quoting .440/.624 beside .430/.687 when
   the paper's own primary values are .383/.589. Every window has a label and every comparison names
   the window it used. Silent switching is the single most damaging comprehension defect found.

All three are cheaper to fix than the dimensions they cost.
