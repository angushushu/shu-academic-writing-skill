# Section functions

The generic job each section performs in an empirical research article. Venue-specific word
budgets and required sections live in `project/venue-target.md`; the project's own spine
lives in `project/manuscript-blueprint.md`. This file holds only what is field-independent.

## The shape: an hourglass

Daryl Bem's image, and the most useful single picture of an empirical article. The paper
starts broad, narrows to the specifics of what you did, then widens again.

```
  Introduction    ▔▔▔▔▔▔▔▔▔▔  broad: the phenomenon, in ordinary terms
                    ▔▔▔▔▔▔    narrower: what is known, and where it fails
                      ▔▔▔▔    narrower: the specific unresolved question
  Method                ▏▏    the neck — maximally specific
  Results               ▏▏    the neck — maximally specific
  Discussion            ▔▔▔▔  widening: what these results imply
                      ▔▔▔▔▔▔  broader: what changes for the field
                    ▔▔▔▔▔▔▔▔  broad: the smallest important conclusion
```

Two failure modes follow directly. An article that is **narrow at the top** opens inside its
own specialty and never earns a general reader. An article that is **narrow at the bottom**
stops at "our hypothesis was supported" and never says what it was worth. Check both ends
before checking anything in between.

The two broad ends are where a little reach is permitted. The neck is where it is not.

## One-sentence spine

Problem → gap → proposal → test → calibrated result → consequence and boundary.

Draft all seven elements as single sentences *before* drafting any section. If an element
will not compress to one sentence, that is the element to work on.

1. **Problem** — the thing people do, need, or face that the paper helps explain.
2. **Gap** — what current accounts name but cannot yet specify, distinguish, or test.
3. **Proposal** — what this work contributes: a formalization, measure, design, or result.
4. **Test** — the design that can actually discriminate.
5. **Result** — what was observed, sized to the evidence.
6. **Consequence** — what a reader can now understand, predict, or do differently.
7. **Boundary** — what the design cannot establish.

## Abstract

- State population, sample sizes, and design.
- State the key effect with direction and calibrated certainty, with uncertainty where the
  word budget permits.
- Name at least one important design limitation. Venues increasingly require this.
- No promotional adjectives. No claims absent from the body.

## Introduction

1. Establish the broad importance of the phenomenon, in the outer reader's terms.
2. Explain what existing accounts achieve and precisely where they stop.
3. Name the missing testable link — the instability, and what it costs.
4. Introduce the proposed resolution in plain language, then in technical terms.
5. State focused predictions or questions with transparent confirmatory/exploratory status.

Failure modes: opening on the topic rather than the problem; gap worship ("no study has…");
theory parade; method-first value ("we developed X"); background that does not change the
reader's route to the main claim.

### The opening statements

Four rules, after Bem. The last is the one almost everyone violates, and journals are a bad
model for it.

1. Write in prose, not in the field's jargon.
2. Do not drop an unprepared reader into the middle of your theory. Lead them to the formal
   statement of the problem step by step.
3. Use examples to introduce abstract or unfamiliar terms. The more abstract the material, the
   more the example is doing.
4. **Open with a statement about people — not about researchers or their literature.**

The difference in practice:

- Opens on the literature: *"Research on X has focused on A and B."* → the reader learns what
  a subfield has been busy with, which is not a reason to keep reading.
- Opens on people: *"People who hold two incompatible beliefs often feel uncomfortable."* →
  the reader recognizes something true about the world, and the technical apparatus can then
  be introduced as a way of explaining it.

A good opening walks from familiar words, through transitional ones, to the technical term —
so the term arrives already defined by the time it is named. That is a definition delivered
without a definition sentence.

### Who to write for

Aim the Introduction and Discussion at an intelligent reader **outside** your specialty: they
should be able to follow what you did, why, and what was learned, even without expertise in
your statistics or paradigm. Aim the Method and Results one level of expertise below the
journal's core audience — assume the standard tools, introduce the unusual one.

Bem's formulation is that good writing is good teaching, and the techniques should stay
invisible while doing it. This is also the practical route to a venue's "broad significance"
requirement: it is not a matter of adding a grand sentence to the Discussion, but of choosing
where in the hourglass each idea is allowed to enter.

## Method

Each item below is a function, not necessarily a subheading.

- Participants: population, recruitment, allocation, exclusions, ethics, `N` per condition.
- Stimuli or materials: sampling rationale, what was sampled from what.
- Measures: constructs, instructions, scale, sampling rate, preprocessing.
- Coding, if any: unit, variables, coders, training, alignment, missingness, reliability
  computed *before* adjudication, adjudication rule.
- Computational procedure, if any: every parameter that changes the result, plus version.
- Analysis: unit of analysis, model formula, random effects, dependence handling,
  diagnostics, uncertainty, multiplicity, planned/exploratory status, robustness checks.

The test: could a competent stranger regenerate every reported number from the raw data using
only this section and the shared scripts?

## Results

1. Descriptive data and reliability.
2. Checks necessary to interpret the primary model at all.
3. Primary analysis, per outcome, each with its own estimate and conclusion.
4. Heterogeneity and sensitivity analyses.
5. Exploratory analyses, clearly separated.

Report nulls with the same care as favorable effects. Do not collapse distinct outcomes into
one composite claim because the composite reads better. Effect sizes and uncertainty are
central; significance is secondary.

## Discussion

1. Answer the research question in one calibrated paragraph.
2. State the conceptual contribution independently of whether every coefficient reached
   significance.
3. Compare plausible rival interpretations, and say which the design does and does not rule
   out.
4. Address construct, internal, statistical, and external validity — each tied to the exact
   inference it weakens, not as a generic limitations dump.
5. Name the specific next discriminating test.
6. End on the smallest important conclusion the evidence can sustain.

## Rewriting

Two things from Bem worth holding onto, because both are counterintuitive.

**Readers are never wrong as unclarity detectors.** When a colleague says a passage is
confusing, the passage is confusing — by definition, since it confused a reader. Their
proposed *fix* may be wrong, even bad. The detection is not. Do not argue, and do not clear it
up verbally; if you explain it in conversation, they will nod, you will feel resolved, and the
next reader to hit it will be a reviewer who does not nod. The best test reader is someone who
publishes in your field but does not work on your topic.

**Restructuring is not rewording.** Shuffling paragraphs and polishing sentences on screen
feels like restructuring and is not. Real restructuring means cutting whole sections, adding
new ones, sometimes returning to the analysis, and reorganizing to fix one bump in the logic.
A badly built argument cannot be rescued by better sentences — which is the same claim
`core/engineer-argument/` makes from the other direction, and the reason the order of
operations in `SKILL.md` runs value first, sentences last.

A corollary for drafting: do not over-polish a first draft. A sentence perfected over forty
minutes is a sentence you will resist deleting when the paper needs to be rebuilt around it.
