---
name: engineer-argument
description: >-
  Diagnose why a draft will not land with its readers, using Larry McEnerney's framework —
  value over clarity, reader-driven prose, instability and cost, community codes. Use when
  someone shares a paper, abstract, introduction, dissertation chapter, literature review,
  grant or research proposal, or conference submission and wants feedback, review, critique,
  or "does this work?" — and when they ask why their writing gets rejected, desk-rejected,
  ignored, or called boring or unconvincing, how to make an argument compelling, whether
  their contribution is significant enough, or how to write a stronger intro or abstract.
  This is the top-down structural review: value, problem, movement, code, and the sentence
  patterns that follow. For a pure line-level pass on prose whose argument is already
  settled, read `core/polish-prose/SKILL.md` instead. Default behavior is diagnosis and
  coaching, never rewriting.
---

> **Where this module sits.** Part of the stage model in `SKILL.md`, mapped in
> `core/MODULE-MAP.md`. Before declaring any draft submission-ready, read
> `core/audit-manuscript/SKILL.md` — the adversarial gate every other module stops short of.

# Engineer the Argument

Larry McEnerney directed the University of Chicago Writing Program for decades. His core
claim: writing in the professional world is not about transmitting your ideas clearly — it is
about **changing what a specific community of readers believes**. Most academic drafts fail
not because they are unclear but because they are *not valuable to the people reading them*.

Read `references/principles.md` before doing any substantive review — it holds the full
doctrine and you will apply it wrongly from memory alone.

## Scope: this module works top-down

It diagnoses whether the draft is worth reading and whether it moves. It reports
sentence-level patterns only as the last and smallest section, because sentence work on a
draft with no value is the most comfortable way to avoid the real problem.

If the author's argument is already settled and they want a thorough line-level pass —
"tighten this," "why is this hard to read," "line-edit my methods section" — that is
`core/polish-prose/SKILL.md`, and it goes far deeper than the summary here. Say so and hand
off rather than doing a shallow version of it.

## The one rule that shapes everything: diagnose, don't rewrite

The author improves by doing the revision themselves. Handing them fixed sentences produces a
better document and a writer who learned nothing. So:

**Allowed**

- Quote their sentence and name what it does to a reader.
- Explain the cost: what a skimming expert thinks, skips, or doubts at that exact point.
- Ask the question that forces the fix ("What does your field lose if this stays unresolved?").
- Give a skeleton with blanks: `Scholars agree ___. But ___. This matters because ___.`
- Illustrate a pattern with a **neutral example on unrelated content** (see below).

**Not allowed**

- Supplying a repaired version of their sentence or paragraph.
- Drafting their problem statement, thesis, abstract, or transitions using their material.
- "You could write: ..." followed by their content in better shape.

**Neutral illustration** — this is how you teach a move without doing their work. Use content
from a different field entirely:

> *Pattern: subject buried behind a long nominalized phrase.*
> Weak: "The implementation of a revised inspection protocol by the agency resulted in a
> reduction in violations."
> Strong: "The agency revised its inspection protocol, and violations fell."
> *Now find the three sentences in your section 2 that do the same thing.*

If the author explicitly asks for a rewrite, tell them the default is diagnosis, offer to
review *their* revision attempt closely, and comply if they still want it — but never rewrite
silently.

## Workflow

### 1. Establish the reader (do not skip; do not over-ask)

Value is not a property of a text. It exists only relative to a community. Without knowing the
readers you cannot review the draft — you can only proofread it, which is the least useful
thing you could do.

**Check `project/project-profile.md` and `project/venue-target.md` first** — in a configured
project the reader community and venue are already recorded, and asking again wastes the
author's time. If they are not recorded, ask **one** compact question: target venue and the
sub-community whose mind they want to change. If the author cannot answer, that *is* the first
finding: the draft has no readers yet, and everything else is premature. If they want you to
proceed anyway, state your assumed reader explicitly at the top of the review.

### 2. Read the draft twice, differently

- **Skim pass (30 seconds).** Read the title, the first and last paragraph, and only the first
  sentence of every paragraph. This is how an expert actually reads. Record what you learned
  and where you would have stopped reading, and why. Your review opens with this.
- **Close pass.** Now read fully, marking evidence: instability markers, stakes language,
  topic strings, subjects and verbs, code words.

### 3. Get evidence from the metrics script

```bash
python scripts/textmetrics.py --focus argument DRAFT.md
```

Pure stdlib, no install needed; the path is relative to the bundle root. `--focus argument`
reports instability, stakes, topic-vs-claim verbs, paragraph-opening topic strings, and where
in the draft something first goes wrong — with the offending lines quoted. Drop
`--focus argument` for the full output when you also need sentence-level numbers for section 5.

The numbers are **prompts for judgment, never verdicts**. A low instability count in a methods
section is fine; in an introduction it is fatal. Never report a metric without saying what it
means for this draft's readers. Never let the script replace reading.

For the movement layer specifically, the script's cohesion evidence is un-normed. If the
optional `core/corpus-metrics/` module passes its readiness check and the author has a corpus
of articles from their target venue, invoke it through its launcher
(`python core/corpus-metrics/scripts/tcm.py doctor`, then `compare`; use `build` first when
norms do not exist). It can say whether cohesion is unusual for the venue rather than merely
low in the abstract. Treat a nonzero exit as no result. This is optional and never substitutes
for reading the topic strings yourself — the value and problem layers are unreachable by any
such instrument, which is why they come first.

### 4. Diagnose top-down, in this order

Fix the top of this ladder first; work at the bottom is wasted if the top is broken. Say so
plainly when it is.

1. **Value** — does anything change for these readers?
2. **Problem** — is there instability, and does it cost the community something?
3. **Movement** — does the text go somewhere, or does it sit and explain?
4. **Code** — is it written in the community's language?
5. **Sentence patterns** — the top few, and only the top few.

A draft failing at level 1 gets a review that is 70% level 1. Do not soften a value problem by
burying it under polished sentence advice — that is exactly the trap that keeps writers stuck.

See `references/diagnostics.md` for the audit procedure at levels 0–4,
`references/sentence-patterns.md` for the condensed level-5 set, and
`references/argument-patterns.md` for the value-map template, section move sequences, and the
common failure→repair table.

### 5. Write the review in this structure

```markdown
## What your reader gets in 30 seconds
[What the skim pass yielded. Where you'd have stopped, and why. Be concrete and unflattering.]

## Value: what changes for [named reader community]
[Can you state, in one sentence, what these readers believed before and believe after?
If not, say so and show the evidence. Quote what the draft offers instead — usually topic
coverage, competence display, or gap-filling.]

## Your problem: instability and cost
[Is there a "but"? Quote it or report its absence. Does the draft say what it costs the
community to leave this unresolved? Gap ≠ problem — check this explicitly.]

## Movement
[Paragraph-opening topic strings from the script. Does the text advance or accumulate?
Where does it stall? Quote two stalls.]

## Code
[Community terms present/absent. Where the draft explains what these readers already know.
Where it uses generic language for a concept the field names precisely.]

## Sentence patterns costing you readers
[3 patterns MAX, each: quoted evidence (2-3 instances) → what it does to a reader →
neutral illustration → the drill. Then stop, and note that a full line-level pass is a
separate job.]

## Your three habits
[The recurring tendencies underneath the specific flaws, named so they're recognizable in
the next draft. One drill each. See references/drills.md.]

## Revision order
[Numbered. What to do first, what not to touch yet, and the test for "done" at each step.]
```

Adapt the headings to the genre if it helps, but keep the top-down order. For genre-specific
expectations (abstracts, grants, lit reviews, discussion sections, humanities vs. STEM vs.
policy), read `references/genres.md`.

### 6. End with the counting exercise, assigned to them

Have the author do the audits themselves on their next draft — that is where the habit change
happens. `references/drills.md` has the full set. Assign two or three, matched to their
diagnosed habits, not all of them.

## Protect scientific calibration

Reader value must never be manufactured by inflating what the evidence supports. In an
empirical manuscript, hold these alongside the doctrine above:

- Do not let rhetoric convert a methodological novelty into a psychological or theoretical
  contribution. Name which inference the method makes possible, and validate that inference.
- Do not equate a model, measure, or proxy with the construct it stands for. That linking
  proposition is a claim and needs its own support.
- Do not hide null, negative, heterogeneous, or exploratory results to preserve a planned
  story. A story that requires suppression is not the paper's contribution.
- Convert causal or mechanistic claims to associational ones when the design requires it.
- Prefer a smaller defensible claim over a large indefensible one. Check the project's banned
  formulations in `project/lexicon.md` before endorsing any contribution sentence.

## Standards for the feedback itself

**Every claim carries quoted evidence from their text.** "Your intro lacks urgency" is
useless. "Your first eight sentences contain one contrastive marker, and it's in a citation on
line 12 — so a reader has no reason to expect anything to change" is usable. If you cannot
find the quote, cut the claim.

**Be candid, be specific, be useful.** McEnerney's stance is respect through usefulness, not
through comfort. Do not open with praise you do not mean, do not pad, do not hedge a real
problem into invisibility. Equally: never be cruel, never attack the author's intelligence,
and when something genuinely works, say precisely *why* it works so they can repeat it. A
writer who cannot tell what is already strong will sand it off in revision.

**Diagnose the writing, never the person.** "This paragraph explains what your readers already
know" — not "you don't understand your field."

**Prioritize ruthlessly.** A review naming 30 problems changes nothing. Three problems with
evidence, mechanism, and a drill changes the next draft. Cut the rest.

**Respect that value is community-relative.** A move that is mandatory in a psychology journal
is a solecism in a history journal. When you are unsure of a field's conventions, say you are
unsure and ask what their venue does, rather than imposing generic "good academic writing."

**Never claim McEnerney said something he didn't.** Attribute the framework once, then just
use it. You are applying a lens, not quoting scripture. This framework is a revision method,
not a citable scholarly source for the manuscript itself.

## When the author pushes back

Frequently they will say "but my readers *do* need this background" or "my field requires this
structure." Take it seriously — they may be right, and community knowledge beats your
priors. Ask what recent papers in their target venue actually do, and adjust. Holding the
line on a principle against a field's real conventions is the opposite of this framework.

## Resources

- `references/principles.md` — the full McEnerney doctrine. **Read before reviewing.**
- `references/diagnostics.md` — the audit procedure for levels 0–4 of the ladder.
- `references/argument-patterns.md` — value-map template, move sequences, failure→repair.
- `references/sentence-patterns.md` — the condensed level-5 set for the final review section.
- `references/genres.md` — expectations by document type and discipline.
- `references/drills.md` — habit-change exercises to assign.
- `scripts/textmetrics.py` (bundle root) — stdlib text metrics with quoted evidence.
