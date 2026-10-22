---
name: audit-manuscript
description: >-
  Conduct an independent, adversarial pre-submission audit of an empirical manuscript against
  editorial fit, claim–evidence alignment, methods and statistics, transparency and
  reproducibility, theory, citations, and prose. Use for reviewer simulation, desk-rejection
  risk assessment, red-team review, submission-readiness gates, or producing a prioritized
  revision memo. Do not use to rewrite the paper, and never resolve an evidence conflict in
  the authors' favor.
---

> **Where this module sits.** Part of the stage model in `SKILL.md`, mapped in
> `core/MODULE-MAP.md`. Before declaring any draft submission-ready, read
> `core/audit-manuscript/SKILL.md` — the adversarial gate every other module stops short of.

# Audit the Manuscript

The adversarial gate. Run it before any draft is called submission-ready.

Read `references/editorial-rubric.md` and `references/reporting-checklist.md`. Before
evaluating any numerical or compliance claim, also read `project/evidence-ledger.md` and
`project/venue-target.md` — auditing numbers without the ledger produces confident nonsense.

## Maintain independence

This is the part that makes the audit worth running, and the part most easily lost.

- Evaluate the manuscript that exists, not the paper the authors intend to write.
- Do not reward novelty language, small `p` values, or large observation-row counts.
- Treat contradictions, missing provenance, and unverifiable claims as findings, not as
  details to be resolved sympathetically.

## Run it in two passes

An audit run on a manuscript that is not yet ingestible produces a category error: it grades a
missing table against an unsupported causal claim as though they were comparable risks, and it
spends the whole review on clerical problems the author already knew about. So the audit has two
passes and the first can halt it.

### Pass 1 — ingestion screen (deterministic; may halt)

Run `scripts/intake_screen.py DRAFT.md`. It reports only defects that stop a submission at the
editorial office, before any reviewer reads the science:

- word ceiling exceeded against the venue profile;
- a required statement or section present as a heading but empty;
- a table or figure the text refers to that does not exist;
- an unresolved citation placeholder — `(REF)`, `(Author, year)`, `[citation needed]` — or a
  document that cites sources and contains no reference list at all;
- drafting markup left in the body (`[[TODO: …]]`, `[why this matters — to fill in]`, `<Table N
  here>`).

**A blocker means the verdict is `intake_rejected` and the audit stops there.** Report the
clerical list and do not run the review lanes. There is no value in grading the argument of a
manuscript that cannot be submitted, and doing so buries the intake problems under a findings
table.

The script also reports **advisories** — things it noticed that are defects rather than intake
failures. Advisories do **not** halt the audit: carry them into Pass 2 and let them be graded
there. The distinction matters because a screen that halts on every imperfection never opens, and
an audit that never opens is a clerical triage tool.

Do not treat a clean screen as a pass. It sees markup and arithmetic and nothing else. The
failure that actually sinks papers — an inference the design cannot carry, written in careful
prose — is invisible to it, which is why Pass 2 exists.

### Pass 2 — substantive audit (five lanes)

Runs **only** if Pass 1 found no blocker. Advisories come with you.

1. **Editor / broad significance.** Is there one important change for readers? Is it
   intelligible outside the subfield? Would this look like a method demonstration better
   suited to a specialist venue?
2. **Theory / construct validity.** Are the constructs, their operational measures, and their
   proxies distinguished throughout? Does each theory invoked generate a tested function, or
   is it decoration? Audit the cited literature too, not only the study — read
   `references/source-quality.md` for opinion-versus-evidence, preponderance, secondary-source
   drift, and whether each conclusion's strength matches its source's.
3. **Design / statistics.** Are inference level, stimulus sampling, repeated measures, time
   trends, autocorrelation, analytic flexibility, model assumptions, uncertainty, and
   heterogeneity handled — and does the stated model match the actual code and grouping
   variables?
4. **Transparency / reproducibility.** Can every number be regenerated from raw data with
   documented scripts and a recorded environment? Are materials, coder records, exclusions,
   preregistration, ethics, AI use, and access constraints disclosed?
5. **Writing / compliance.** Does the structure meet the venue's current rules? Are abstract,
   word budgets, citations, claim calibration, and statistical style compliant?

## Assign severity

Severity applies to Pass 2 findings. Pass 1 findings are not graded on this ladder at all —
they are intake failures, and ranking them against scientific defects is the category error the
two-pass split exists to prevent. There is therefore **no `blocker` grade**: a defect severe
enough to stop the submission is an intake failure and belongs to Pass 1's verdict, not to a
grade on this ladder. When you find yourself wanting to write `blocker`, check whether the item
is in fact an ingestion failure.

Grade by **what the defect does to the paper**, not by how long the fix would take.

- **Major** — creates a likely desk-rejection or reviewer objection, or materially weakens the
  inference.
- **Moderate** — impairs clarity, completeness, or credibility.
- **Minor** — copy, formatting, or presentation.

Do not let "this would be easy to fix" pull a finding down a level. Repair effort is not an
outcome, and grading on it makes two reviewers disagree about items they both spotted.

## The repair column

The required output asks for the *smallest adequate repair*. Read that as **a quoted edit inside
a finding**, which is a different activity from drafting the author's prose. The bundle's
prohibition on rewriting governs composing text the author will use as their own; naming a
substitution the author can accept or reject does not do that. What follows from the distinction:

**When the repair reworks material already in the manuscript, give the text.** A clause, a
sentence, a deletion. `"delete"` is a complete and often correct answer.

**When the repair needs a fact, number, citation, or record the manuscript does not contain,
name what must be supplied and stop.** Do not generate it, not even as a plausible illustration.
`"replace (REF) with the citation for the induction protocol, or delete the clause asserting a
standard protocol"` is complete. `"t(40) = 2.45, p = .018"` offered as a sample is fabricated
provenance and is forbidden however clearly it is labelled.

The test: **could the author apply this without discovering anything new?** If applying it would
require inventing a source, it is not a repair — name the missing evidence and leave it to them.

## Required output

**Report every finding. There is no cap on the number of findings.**

This was wrong before, and it cost measured coverage. The audit used to ask for the "three
strongest features" and a ranked sequence of three actions, matching a triage deliverable that
answers "what should I fix first". On a real manuscript with 24 verified defects, that cap was the
dominant limit on how many defects a reviewer located: lifting it nearly **doubled** location
coverage (0.323 → 0.616 without the method, 0.167 → 0.425 with it). A reviewer that finds fifteen
problems and reports three has not triaged; it has discarded twelve.

An audit is the comprehensive form. If you are asked for a short list, that is a *different*
deliverable and should be labelled as one.

Machine-readable verdict identifiers are given in brackets. A downstream tool reads those exact
strings; the prose form is for the author. Emitting a paraphrase of either one fails silently,
because a comparison that never matches produces no error.

1. **Verdict:** `intake_rejected` [`intake_rejected`], `not ready` [`not_ready`],
   `conditionally ready after blockers` [`conditionally_ready`], or
   `submission-ready on available evidence` [`submission_ready`].
2. **Findings** — every problem found, not a selection. For each: severity, location, the claim
   or rule at issue, a verbatim span, evidence, consequence, smallest adequate repair. Order them
   by risk removed so the most consequential comes first, but do not truncate the list.
3. **Priorities** — if the author asked what to fix first, name up to three of the findings above
   by position. An ordering over the full list, not a replacement for it.
4. **What works** — specific, with the mechanism. An author who cannot tell what works will sand
   it off in revision. Keep it brief; it is not the deliverable.
5. **Claim ledger** using the project's `DESIGN` / `OBSERVED` / `INFERENCE` / `PLANNED` labels
   (see `core/develop-manuscript/references/provenance-rules.md`).
6. **Reproducibility and venue-compliance checklist**, from `references/reporting-checklist.md`.
7. **Remaining uncertainties** that require the author, original study documentation, or a
   rerun to settle. Name them; do not guess past them.

**Fabricate nothing.** Every finding carries a span that appears verbatim in the manuscript. That
instruction is not decoration — it is the one measured effect of reading this module. In the
benchmark above, reviewers that did not read it quoted text appearing nowhere in the manuscript in
8 of 9 runs; reviewers that did, in 3 of 10. A finding you cannot quote is an uncertainty: item 7.

## Screening scripts

Run these as one screen among several, then inspect every flagged passage manually and add
the issues no script can detect.

```bash
python scripts/audit_draft.py DRAFT.md --patterns project/claim-risks.md
python scripts/check_manuscript.py DRAFT.md --profile project/venue-target.md
```

A clean script run is not a passing audit. These catch lexical and structural risks only:
they cannot see an unsupported inference written in careful prose, which is the failure mode
that actually sinks papers.

## What this pass is not

This is a **correction** pass, not a style pass, and the distinction was measured. Run by the same
author on a finished draft, an audit that adds explanatory blocks -- a full-series estimates section,
a second window in every table, a renormalisation paragraph -- raises mechanical compliance from 4/12
to 9/12 and **lowers a reviewer's preference for the paper from 92% to 25%** against the comparison
skill, while the comparison skill with the *same* 9/12 compliance is preferred 9-3.

The content is not the problem. Reviewers credited the comparison skill for reporting both windows
and penalised this bundle for "two windows in every table". The difference is that required
disclosure was written into the sections that exist for it, while the audit inserted it into the
argument.

So: fix what is objectively wrong -- a number that does not reconcile, a citation with no entry, an
analysis promised and not reported, a marker left in the text -- and prefer the smallest edit that
does it. **Do not add an explanatory paragraph to the middle of a case.** If a disclosure is missing
and the venue requires it, it belongs in the venue's own section, and the place to write it is the
draft, not this pass.
