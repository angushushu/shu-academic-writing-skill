# Diagnostic Procedures

How to run each level of the ladder. Work top-down; report top-down. Each audit tells you what
to collect, what the failure looks like, and what to write.

## Contents

1. [Level 0: the skim pass](#level-0-the-skim-pass)
2. [Level 1: value audit](#level-1-value-audit)
3. [Level 2: problem audit](#level-2-problem-audit)
4. [Level 3: movement audit](#level-3-movement-audit)
5. [Level 4: code audit](#level-4-code-audit)
6. [Level 5: sentence audit](#level-5-sentence-audit)
7. [Reading the metrics honestly](#reading-the-metrics-honestly)
8. [Writing feedback that teaches](#writing-feedback-that-teaches)
9. [Worked example of a finding](#worked-example-of-a-finding)

---

## Level 0: the skim pass

Before reading properly, simulate the real reader. Read only: title, abstract if present, the
first sentence of every paragraph, any headings, the first and last paragraph.

Record three things:
- **What you learned.** Write it as a sentence. Usually it's a topic, not a claim — that fact
  alone is a finding.
- **Where you would have stopped.** Name the paragraph and say what made you leave: nothing
  at risk, information you already had, an unpaid promise, a wall of setup.
- **What you expected next at that point, and whether you got it.** Broken expectations are
  where readers exit.

Do this before the close read. Once you've read carefully you can no longer simulate the skim,
and the skim is the reading that decides your author's fate.

## Level 1: value audit

**Collect:** every sentence that asserts why the work matters. Every occurrence of *important,
significant, crucial, contributes, sheds light, adds to our understanding, fills a gap.* The
stated purpose sentence ("This paper examines/explores/discusses/describes...").

**Test:** complete this from the text alone, using only what's on the page:

> Readers in ______ currently believe ______. After this paper they will believe ______.
> Because of that change, they will do ______ differently.

Failure looks like:
- The middle blank fills with a topic ("they'll know more about municipal water pricing").
- The third blank cannot be filled at all.
- The verb in the purpose sentence is a *topic verb* — examines, explores, discusses,
  describes, looks at, investigates, presents, provides an overview of — rather than a *claim
  verb* — argues, shows, demonstrates, challenges, revises, complicates, explains why,
  overturns.
- Value is asserted for the world rather than for a community ("water access is a pressing
  global issue"). Global importance is not reader value; the world does not read journals.
- Value is autobiographical: "I became interested in," "this project grew out of."

**Report:** quote the purpose sentence, show which blank fails, and ask them the question
directly. Do not fill the blanks for them. Often the value exists in the author's head and has
simply never been written down — a question surfaces it; a rewrite hides that it was missing.

## Level 2: problem audit

**Collect:** all contrastive markers in the opening (the script counts and quotes them). All
cost/consequence language. The first sentence where anything is at risk — note its position by
paragraph number.

**Test the four-part engine** (stability → destabilization → cost → resolution). Check each
part is present, in the opening, and in the readers' terms.

Failure patterns, each with a distinct fix:

| Pattern | Signature | What to ask the author |
|---|---|---|
| No instability | Zero contrastive markers in the first page; a topic tour | "What does your field currently get wrong, and where does it break?" |
| Instability with no cost | A clear "but," no consequences | "If nobody resolves this, what specifically goes wrong for these readers?" |
| Gap framing | "little attention has been paid to" | "So what? Answer it as if a hostile reviewer asked." |
| Late problem | The real tension appears on page 6 | "Your paper starts on page 6. What's paragraph 1 doing?" |
| Someone else's problem | Stakes belong to practitioners while venue is theoretical (or vice versa) | "Whose problem is this, and do they read this journal?" |
| Manufactured stakes | Grand claims disproportionate to the finding | "What's the smallest true version of this claim?" |

**Report:** quote the strongest instability sentence in the draft, wherever it is. If it's on
page 6, that's the headline finding. If there isn't one, say so with the count as evidence.

## Level 3: movement audit

**Collect:** first six words of every paragraph (the script prints this list). Every paragraph
opening that starts with an additive connector. Section headings.

**Tests:**
- **Topic-string read.** Read the openings in sequence. Argument advancing, or table of
  contents? Circling on one topic?
- **Additive count.** *Additionally, Furthermore, Moreover, Another, Also, In addition* opening
  a paragraph means accumulation. Two or three across a paper is normal; a pattern is a
  structural finding.
- **Deletion test.** Pick two middle paragraphs and ask what breaks if they're deleted. If
  nothing breaks, they're accumulation, not argument.
- **Order test.** Could the paragraphs of a section be shuffled without loss? Then the section
  is a list. Lists are fine for genuinely parallel material and fatal for argument.
- **Promise tracking.** Note every promise the opening makes ("I first show... then...").
  Check each is paid, in order. Unpaid promises are where readers stop trusting.

**Report:** paste the topic-string list — authors find it startling to see their own paper's
skeleton — and quote two specific stalls with what happens to a reader there.

## Level 4: code audit

**Collect:** technical terms used; concepts explained; citations and their vintage; any
definition of a standard term.

**Tests:**
- **Explaining the known.** Flag every passage defining something the target community uses
  daily. Quote one and ask who it's for.
- **Generic-where-precise.** Flag places using ordinary words for concepts the field names.
  You often cannot know the right term — say so and ask: "Your field has a name for this. Is
  it in your draft?"
- **Conversation vintage.** Citations mostly to textbooks, handbooks, or work older than a
  decade suggests the author is addressing the field's settled knowledge rather than its live
  argument.
- **Costume test.** Delete the technical vocabulary from a dense paragraph. If no claim
  survives, the terms were doing decorative work.

**Report:** be explicit about the limits of your knowledge of their subfield. Ask rather than
assert when the convention is uncertain.

## Level 5: sentence audit

Patterns are in `sentence-patterns.md`. Two constraints on how you report:

- **Maximum 3 patterns.** Choose by frequency × cost. A pattern appearing twice is not worth
  a section; one appearing in half the sentences is the whole game.
- **Pattern, not instance.** The goal is that they can find the sixth instance themselves.
  Give 2–3 quoted instances so the pattern is visible, then stop listing.

Never open a review at this level. If the draft has no readers and no problem, sentence advice
is a distraction the author will gratefully accept in order to avoid the real work.

A structural review is also not the place for a thorough line pass. If the argument is settled
and the author wants every sentence looked at, say that is a different job and name the
`core/polish-prose` module, which carries the full pattern set and its drills.

## Reading the metrics honestly

The script gives densities per 1,000 words. Interpret against the section's job:

- **Instability markers** — an introduction or discussion with near-zero density is a real
  finding. A methods section with near-zero density is correct. Never flag it there.
- **Nominalizations** — high density in a theory-heavy humanities piece may be idiomatic; in a
  results narrative it's usually agency being hidden. Look at whether the actors are visible.
- **Hedges** — some fields require heavy hedging and some read it as weakness. Clustering is
  more telling than the count: three hedges in one sentence signals the author doesn't believe
  their own claim.
- **Passive constructions** — not a flaw. Passive is correct when the recipient is the topic or
  the agent is genuinely irrelevant. Only flag passives that hide an agent the reader needs.
- **Sentence length** — the mean matters less than the variance. Uniformly long sentences read
  as undifferentiated; the absence of any short sentence means no claim ever lands hard.

Say what a number means for this draft, or don't report it.

## Writing feedback that teaches

Each finding has four parts, in this order:

1. **Evidence** — their words, quoted, with a location.
2. **Mechanism** — what happens in a reader's head at that point. Not "this is vague" but "a
   reader has to hold three unresolved referents until the verb arrives in line 4."
3. **Illustration** — neutral before/after on unrelated content, showing the move.
4. **Assignment** — what they do, phrased as a question or a search task.

Skipping (2) produces a rulebook they can't generalize from. Skipping (4) produces agreement
without change.

**On praise:** identify what genuinely works and explain the mechanism, exactly as with flaws.
Untargeted praise ("nice flow!") is noise; targeted praise ("your third paragraph opens with
the term you ended the second on, which is why it reads as advancing") is a transferable
lesson and prevents them from destroying their strengths in revision.

## Worked example of a finding

> **Your opening pays for context it doesn't spend.**
>
> Paragraph 1 runs 180 words and its first four sentences are: [quoted]. Every one of these
> states something a reader of *[venue]* accepted before graduate school. Your first
> contrastive marker is "however," in line 19 — by which point a skimming reviewer has read
> your title, this paragraph, and left.
>
> What happens mechanically: an expert reads to find the risk to their beliefs. Sentences that
> restate consensus signal "nothing here for you," and the cost of continuing rises with each
> one. They are not being lazy; they are triaging thirty papers.
>
> *Illustration, from a different field:* an opening that begins "Cities have grown rapidly
> since 1950" tells an urban economist nothing. One that begins "Rapid urban growth should
> have raised land prices uniformly, but three of the fastest-growing metros saw them fall"
> puts something at risk in the first sentence.
>
> **Your move:** find the sentence in your draft where something first becomes unsettled — I
> think it's the one starting "Yet the 2019 data..." on page 3. Ask why it isn't your first
> sentence, and what of paragraphs 1–2 survives if it is.
