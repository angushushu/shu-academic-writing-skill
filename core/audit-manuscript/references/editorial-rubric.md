# Editorial and reviewer rubric

Score each item `0 = absent/invalid`, `1 = major weakness`, `2 = adequate`,
`3 = unusually strong`. A high total cannot compensate for a blocker.

Venue-specific limits (word budgets, reference counts, required sections, style) are not
duplicated here — read them from `project/venue-target.md`. Project-specific blocker
candidates live in `project/claim-risks.md`.

## General contribution

- The problem matters to the venue's broad readership, not only to the immediate specialty.
- The contribution changes an explanation, a measurement possibility, or a research program —
  rather than merely adding a tool or a dataset.
- The paper remains valuable under null or mixed results.
- Naturalistic realism, where claimed, is paired with calibrated validity and generalizability
  rather than used to excuse them.

## Theory and constructs

- One primary theoretical spine organizes the paper.
- Every secondary theory performs a distinct, necessary function.
- Construct-to-measure linking propositions are explicit and falsifiable.
- A model, graph, index, or proxy is never silently equated with the construct it stands for.
- Distinct outcomes are kept distinct, with their own predictions and interpretations, rather
  than merged into a composite that reads more cleanly.
- Alternative explanations are named and, where possible, benchmarked.

## Design and inference

- Claims match the design's actual inferential reach.
- Levels are separated throughout: participants, observations, stimuli, units within stimuli,
  and time points.
- A small or purposive stimulus sample is not obscured by dense repeated observations.
- Shared time trends, autocorrelation, smoothing or alignment choices, and between-unit
  heterogeneity are addressed.
- Model choices and robustness checks were not selected after seeing favorable results
  without disclosure.
- Null, negative, and inconsistent findings receive symmetric reporting.

## Evidence and reporting

- Final numerical claims trace to one reproducible pipeline.
- Effect sizes and uncertainty are central; significance is secondary.
- Coding or annotation reliability matches the actual coding design, and is reported before
  adjudication.
- Analysis assumptions, exclusions, missingness, scaling, and multiplicity are clear.
- Results in the abstract, figures, text, supplement, and scripts agree.

## Transparency and reproducibility

- The venue's required transparency statement is complete and current.
- Materials, primary data, processed data, code, codebook, environment, and run instructions
  are shareable, or the constraints are justified.
- A clean run reproduces the manuscript's numbers and figures.
- Preregistered and exploratory decisions are accurately separated, with the real chronology.
- AI assistance is logged and disclosed; humans verified all outputs.

## Writing and venue fit

- The abstract meets the venue's limit and includes population, sample size, and at least one
  major design limitation.
- Counted word budgets are met.
- The broad problem precedes any method terminology.
- Prose is economical, concrete, and calibrated.
- References perform clear functions rather than demonstrating coverage.
- The manuscript is anonymized where required and follows the venue's style manual.

## Generic automatic-blocker candidates

Any one of these is a blocker regardless of the rest of the score.

**Blocker here is a verdict, not a grade.** These belong to the ingestion screen and its
`intake_rejected` verdict, not to the severity ladder — the ladder is major / moderate / minor.
The distinction matters because "blocker" is used in two senses in review work: as a
disqualifier that no total score can offset (this list), and as a top severity tier (which this
bundle deliberately does not have).

- Manuscript numbers are drawn selectively from conflicting outputs.
- A main result cannot be rerun from documented inputs and code.
- Repeated within-unit observations are presented as independent sample `N`.
- The procedure described in Method differs from the executed code.
- A mental state, mechanism, or unobserved construct is claimed as measured when only a proxy
  was observed.
- Distinct outcomes with divergent results are summarized as one pattern.
- Raw or primary data, materials, or scripts are unavailable without a stated and defensible
  transparency constraint.

Add project-specific blockers from `project/claim-risks.md`.
