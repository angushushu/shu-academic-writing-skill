# Provenance rules

The discipline that keeps a growing draft honest. These rules are field-independent; the
project's actual verified numbers live in `project/evidence-ledger.md`.

## Source-of-truth hierarchy

When two artifacts disagree, the higher tier wins — and the disagreement still gets reported.

1. Raw and primary data; original coder or instrument records.
2. Versioned analysis scripts and the outputs regenerable from those data.
3. Statistical and reliability reports traceable to a specific script and run.
4. Slides, READMEs, prediction notes, prose summaries, and draft claims.

Conference decks and READMEs are tier 4. They are recollection, not evidence. A number that
exists only in a deck is not yet a result.

## Evidence-status vocabulary

Tag every numerical claim with exactly one status. Use these labels verbatim so they are
greppable across the project.

- `VERIFIED_CURRENT` — regenerated from named current inputs and code, with command and
  output artifact recorded.
- `AUTHOR_CONFIRMED_CANONICAL` — selected by the project lead and matched to current code,
  but still awaiting a machine-readable rerun artifact.
- `HISTORICAL_ALTERNATIVE` — valid provenance from abandoned parameters, metrics, or analysis
  plans. Not current evidence.
- `UNVERIFIED_NARRATIVE` — stated in prose, README, or outline without a traceable output.
- `ABANDONED_PIPELINE` — a superseded analysis path retained only for provenance.

Nothing becomes `VERIFIED_CURRENT` without: source data, script, exact command, output path,
run timestamp or hash, unit of analysis, and every relevant `N` definition.

## Claim-type vocabulary

Tag every substantive claim in the ledger:

- `DESIGN` — what the study or model was constructed to do.
- `OBSERVED` — directly supported by a traceable artifact.
- `INFERENCE` — an interpretation requiring explicit linking assumptions.
- `PLANNED` — a proposed analysis or claim not yet completed.

The common failure is an `INFERENCE` written in the grammar of an `OBSERVED`.

## Exploration and the confirmatory record

Daryl Bem's widely taught advice on empirical articles opens by asking which of two papers you
should write: the one you planned before collecting data, or the one that makes sense now that
you have seen the results. He answers: the second. He recommends exploring the data from every
angle, and, if the findings warrant, recentering the article on what you found and
subordinating the original hypotheses.

**Half of this is right and worth keeping.** Discovery has no formal rules; exploration is how
findings get noticed at all; and a paper genuinely should not be a chronological tour of the
author's abandoned hunches. There is no statistical correction for failing to look.

**Half of it is now known to cause serious harm.** Recentering a paper on a post hoc finding
*and presenting it in the grammar of a prediction* is HARKing — hypothesizing after results are
known. It is one of the practices the replication crisis identified as a principal source of
unreplicable literature, and selective venues now screen for it directly under headings like
analytic flexibility and researcher degrees of freedom. Read that section of Bem as a document
of pre-2011 norms, not as current guidance.

**The rule that resolves the tension.** Exploration is not the problem; *concealing the
chronology* is. So:

- Explore as freely as the data allow. Then label what you found as exploratory and say so in
  the text, not only in a supplement.
- A finding may absolutely become the centerpiece of the paper. It may not acquire a
  predictive tense on the way there.
- Where a hypothesis was genuinely preregistered or pre-specified, say which, and where the
  record is. Where it was not, say that too.
- Report disconfirming results for hypotheses the field actually cares about. Bem's own
  exemption — "if nobody cares about the hypothesis, nobody cares that you were wrong" — is
  only safe for genuinely exploratory work that is *labeled* as such.
- Dropping participants, trials, or observers because they produced anomalous results is not a
  reporting choice. Every exclusion needs a rule, a count, and a stated point in time at which
  it was decided.

**The test.** Take any claim in the draft and ask: could a reader tell, from the manuscript
alone, whether this was predicted or discovered? If not, the manuscript is making a
confirmatory claim it has not earned — regardless of whether the underlying finding is real.

## Never invent

Not from plausibility, not from convention, not as a placeholder that will "obviously" be
fixed later: citations, DOIs, coefficients, confidence intervals, sample sizes, coder
agreement, exclusion counts, preregistration status, ethics approval, power justification,
data availability, or repository links.

If a number is needed and unavailable, write an explicit unresolved marker and list it in the
handoff. A marked gap is recoverable; a fabricated number that survives into submission is
not.

## Handling conflicts

Stop and document. Trace the generating script, or rerun the smallest relevant analysis.
Record which artifacts disagree, by how much, and why — mismatched parameters, different
subsetting, an abandoned plan, a transcription error.

Do not reconcile by averaging. Do not pick the favorable one. Do not quietly drop the
inconvenient one. Superseded outputs are not deleted; they are labeled with their provenance
and status.

## Levels of analysis

Keep these distinct in every sentence, table, and figure caption:

- **Participants** — people. This is `N`.
- **Observations** — repeated records, rows, time points, trials. Never reported as `N`.
- **Stimuli** — the sampled materials. A small purposive stimulus set is a fixed-effect and
  generalizability boundary, and must be discussed as one.
- **Units within stimuli** — scenes, items, dialogue units, segments.

Dense repeated observations do not license precision claims and do not substitute for
stimulus sampling. Verify unique participant counts directly from raw participant data before
submission, not from a derived analysis file.

## File safety

- Do not modify raw data, original coder files, or original response records.
- Do not overwrite existing result files while testing. Write audit and reanalysis outputs to
  a clearly named new directory, recording command, environment, and input files.
- Do not delete superseded outputs. Mark their provenance and status.
- Do not rename or move literature without updating the project's literature inventory.
