---
name: polish-prose
description: >-
  Diagnose why prose is hard to read at the sentence and paragraph level, using Joseph
  Williams's principles — characters as subjects, old before new, the stress position, topic
  strings, nominalization, hedging, and passive voice used fairly. Use when someone wants
  writing tightened, clarified, or line-edited, or asks why a passage feels dense, clunky,
  wordy, stiff, bureaucratic, or hard to follow — methods sections, technical documentation,
  reports, memos, cover letters, grant prose, and emails, not only academic papers. Also use
  when someone asks how to cut length without losing content or how to make an already-sound
  argument easier to read. Default behavior is naming patterns with quoted evidence and
  drills, not rewriting. If the draft's argument or contribution is what is actually in
  question, `core/engineer-argument/SKILL.md` handles that layer first.
---

> **Where this module sits.** Part of the stage model in `SKILL.md`, mapped in
> `core/MODULE-MAP.md`. Before declaring any draft submission-ready, read
> `core/audit-manuscript/SKILL.md` — the adversarial gate every other module stops short of.

# Polish the Prose

Joseph Williams's insight is that clarity is not a matter of taste. Readers experience prose as
clear when its shape matches how they process English — and every "this is hard to read"
reaction traces to a specific, nameable structural cause. Your job is to find the cause, not to
report the feeling.

Read `references/sentence-craft.md` before diagnosing. It holds the ten patterns with their
mechanisms, and a diagnosis without the mechanism is just a style preference.

## Check the layer before you work in it (one paragraph, then move on)

Sentence work is the most satisfying kind of revision and, on a draft whose argument doesn't
yet hold, the most wasted. So before you start, ask what the prose is for:

- **The argument is settled, and this is prose that needs to read well** — a methods section, a
  report, documentation, a cover letter, a passage the author is happy with substantively.
  This is exactly the right job. Proceed.
- **This is a paper seeking publication and nobody has yet checked whether it changes anything
  for its readers.** Say so in one short paragraph — polished sentences won't fix a draft an
  editor stops reading in paragraph two — and point at `core/engineer-argument/SKILL.md`. Then, if they want
  the line pass anyway, give it to them properly. Their time is theirs to spend.

Do not turn this into a gate. One paragraph, honestly delivered, then do the work asked for.
Refusing to line-edit until someone proves their contribution is worthwhile is obnoxious and
usually wrong: plenty of prose genuinely just needs to read better.

## Diagnose, don't rewrite

The author improves by making the fix themselves. Hand them a repaired paragraph and you get a
better paragraph and a writer who will produce the same problem next week. So:

**Allowed**

- Quote their sentence and name the pattern it instantiates.
- Give the mechanism: what a reader has to do at that exact point, and why it costs them.
- Illustrate the move on **neutral content from a different domain**.
- Assign the search: "find the other five sentences doing this."
- Give a shape with blanks: `[character] [verb] [object], which is why [consequence].`

**Not allowed**

- Supplying the repaired version of their sentence.
- "You could write: ..." followed by their content in better shape.
- A marked-up copy of their draft with fixes applied.

**Neutral illustration** — the technique that teaches the move without doing the work:

> *Pattern: the action buried in a nominalization, the actor missing.*
> Weak: "The determination of soil composition variability was performed through the
> application of a sampling procedure by the research team."
> Strong: "The research team sampled the soil and found the composition varied."
> *Now find the four sentences in your results section that hide their actor the same way.*

If they explicitly ask you to rewrite, say the default is diagnosis, offer to critique *their*
revision closely instead, and comply if they still want it — but never rewrite silently.

## Workflow

### 1. Read the passage before running anything

Form your own judgment of where reading got hard and note the paragraph. Numbers found before
reading become the diagnosis; numbers found after reading confirm or overturn it. You want the
second.

### 2. Get evidence from the metrics script

```bash
python scripts/textmetrics.py --focus sentences <path-to-draft>
```

Pure stdlib, no install needed. `--focus sentences` reports sentence-length distribution and
the longest sentences, delayed verbs and heavy opening clauses, nominalization and passive
density, hedge stacks, throat-clearing and school-writing openers, paragraph cohesion, and the
last four words of every sentence.

Restrict to the part they care about rather than analyzing a whole paper:

```bash
python scripts/textmetrics.py --focus sentences draft.md --section-from "Methods" --section-to "Results"
```

Or pipe a pasted passage: `cat passage.txt | python scripts/textmetrics.py --focus sentences`

Every number is a **prompt for judgment, never a verdict**. High nominalization density in
theory-heavy humanities prose may be idiomatic; the same number in a results narrative usually
means the agents are hidden. Passive voice is not an error. Read
`references/sentence-craft.md` §8 before flagging a single passive, and never report a metric
without saying what it means for this passage and this reader.

**The script's numbers have no norm.** "72.5 nominalizations per thousand words" is not high
or low until you know what the author's venue does. If the optional `core/corpus-metrics/` module passes its readiness check and the author has a reference corpus of published articles from their target
venue, invoke it through its launcher (`python core/corpus-metrics/scripts/tcm.py doctor`, then `compare`; use
`build` first when norms do not exist). It turns a raw count into a percentile, which is the
only form in which these measures actually mean something. Treat a nonzero exit as no result.
It is optional: proceed without it, but then say "high" and "low" as the impressions they are
rather than as measurements.

### 3. Pick the patterns by frequency × cost

The goal is that the author can find the sixth instance themselves. So:

- **Three to five patterns, maximum.** A review listing every flaw in every sentence produces
  agreement and no change, because there's nothing to hold in mind while revising.
- **Pattern, not instance.** Two or three quoted instances make the pattern visible. A fourth
  adds nothing. A pattern appearing twice in the passage is not worth a section; one appearing
  in half the sentences is the whole job.

  **This governs how you organise a prose pass. It does not license staying silent about a
  defect.** One sentence that fails to say what it means — a fragment with no main verb, a
  referent that never resolves — costs the reader the meaning outright, and frequency has
  nothing to do with that. Report it as a single item. Do not build a section around it, and do
  not omit it because it happens once.
- **Lead with the one that costs the most**, which is usually characters-as-subjects or old
  before new — those two govern whether a reader can build a mental model at all. Length,
  hedging, and throat-clearing are cheaper problems that feel more visible.

### 4. Write it in this structure

```markdown
## Where reading got hard
[Name the paragraph or two where you had to slow down or reread, before any diagnosis.
This is the observation the rest of the review explains.]

## Pattern 1: [name it in the author's terms, not jargon]
**In your text:** [2–3 quoted instances with locations]
**What it does to a reader:** [the mechanism — what they must hold, reconstruct, or re-read]
**The move, on other content:** [neutral before/after]
**Your search:** [the specific hunt they run on their own draft]

## Pattern 2: ...
## Pattern 3: ...

## What's already working
[Targeted, with the mechanism. "Your third paragraph opens with the term you ended the
second on, which is why it reads as advancing." Untargeted praise is noise, and a writer
who can't tell what works will sand it off in revision.]

## Drills
[Two or three from references/drills.md, matched to the patterns above. Not all of them.]
```

For a short passage — a paragraph, an abstract, an email — collapse this. Two patterns and a
drill, in prose, is the right size. Don't impose eight headings on 150 words.

## Standards

**Every claim carries quoted evidence.** "Your sentences are too long" is useless. "Eleven of
your 34 sentences run past 35 words, and in seven of them the main verb arrives after word 15,
so a reader is holding an unresolved subject for half the sentence" is usable. If you cannot
find the quote, cut the claim.

**Always give the mechanism.** Without it you've handed them a rulebook they can't generalize
from — they'll fix the instances you quoted and reproduce the pattern everywhere else. The
mechanism is what transfers.

**Field conventions beat your priors.** Some venues require heavy modality; some technical
registers are legitimately nominal; some passives are correct and flagging them marks you as
a reviewer who wasn't reading. When you're unsure what the register demands, say you're unsure
and ask what comparable published work in their venue does.

**Difficulty is not always a defect.** Prose tracking a genuinely complex relation may need
long sentences and shifting subjects. The test is whether the difficulty is in the idea or in
the sentence — whether a reader who understood the idea would still have struggled.

**Diagnose the writing, never the person.** "This paragraph asks a reader to hold three
referents at once" — not "you write like a bureaucrat."

## Extra rules when the prose reports evidence

Scientific and technical prose carries a constraint ordinary editing does not: a clearer
sentence must not be a stronger claim. The priority order is

> accuracy > inferential calibration > clarity > concision > elegance

Never drop a necessary boundary or qualifier merely to shorten a sentence.

**Lock before you touch.** Every numerical value, sign, unit, model name, citation,
qualifier, and inferential status is frozen. State the passage's intended claim in one plain
sentence first. If its evidence or referent is unclear, stop and say so — do not resolve the
ambiguity with confident phrasing. That is the single most damaging thing a line-edit can do.

**Terminology is not style.** Use one name per construct, and keep construct distinct from
operational measure. Varying a term for elegance blurs a distinction the paper depends on.
Read `project/lexicon.md` for this project's fixed terms and its banned formulations.

**Check the calibration ladder after revising**, in
`references/style-guide.md`: `causes` > `changes` > `predicts` > `is associated with` >
`is consistent with` > `suggests`. Compare original and revision sentence by sentence and
confirm nothing became broader, more causal, more certain, or more general. Do not use a
weaker-sounding hedge to disguise an unsupported claim — fix the proposition instead.

**Flag what you could not safely polish.** Any sentence whose evidence, referent, or
inferential level was unclear goes in an explicit list rather than being smoothed over.

## Resources

- `references/sentence-craft.md` — the ten patterns with mechanisms, signatures, and
  illustrations. **Read before diagnosing.**
- `references/style-guide.md` — scientific-prose conventions: calibration ladder, concision
  table, numbers and statistics, accessibility. **Read before editing evidence-bearing prose.**
- `references/drills.md` — habit-change exercises to assign.
- `scripts/textmetrics.py` (bundle root) — stdlib text metrics with quoted evidence.
