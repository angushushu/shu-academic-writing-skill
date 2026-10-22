# Submission package

Stage 8. The audit has returned `submission-ready on available evidence`; now the manuscript
has to become a set of files that a portal will accept and a reproducibility checker can run.

Venue-specific requirements are in `project/venue-target.md` and always win over this file.
This is the field-independent scaffold.

## Why this stage gets botched

It arrives when the intellectual work is done and the author is finished caring. Deadline
pressure is at its highest and attention at its lowest, and the failures here are the
embarrassing kind — a supplement referring to a table that got renumbered, a repository link
that resolves to an empty project, an anonymized manuscript with the authors' names in the
file metadata.

Budget real time for it. Treat it as a checklist to execute, not a formality to clear.

## The manuscript file

- [ ] Every word budget met, counted the way the venue counts.
- [ ] Abstract within limit; contains population, `N`, design, key effect, and a limitation.
- [ ] Required statements present and correctly positioned.
- [ ] Every in-text citation is in the reference list, and the reverse.
- [ ] Tables and figures numbered as they are cited, with every cross-reference re-checked
      *after* the last reordering.
- [ ] Every number in the abstract, text, tables, and figures traces to one current output —
      not to a superseded run, and not to a conference deck.
- [ ] Statistical style conforms: decimals, exact `p` values, effect sizes with intervals.
- [ ] Anonymized if required — and check file metadata, not just the visible text.

## The transparency statement

- [ ] Conflicts, funding, ethics approval, and consent.
- [ ] Preregistration: status, link, and the true chronology. If nothing was preregistered,
      say so plainly rather than leaving it ambiguous.
- [ ] Data, materials, and code: where they are, or why they cannot be shared.
- [ ] AI use, at the level of detail the venue requires — see below.

## The reproducibility package

The test: a competent stranger, with only what you deposited, regenerates every reported
number. Not "could in principle" — actually does.

- [ ] Raw or primary data, plus the ready-to-analyze form, with a codebook.
- [ ] Complete preprocessing and analysis scripts, in run order.
- [ ] Environment pinned: language versions, package versions, and any random seeds.
- [ ] A README that runs from inputs to every manuscript output, step by step.
- [ ] An output-to-manuscript crosswalk: which script produces which table, figure, and
      in-text number.
- [ ] A clean-run check from a fresh checkout — not from your working directory, where an
      uncommitted file has been silently holding everything together.
- [ ] Licenses, privacy constraints, and any third-party material whose access route must be
      explained rather than redistributed.

Deposit before submitting, and confirm the link resolves for someone not logged in.

## The AI-use log

Venues increasingly require disclosure of AI assistance in both the research and the writing.
`project/worklog.md` entries carry an `AI` field for exactly this reason — the log is built
incrementally during the work, because reconstructing it at submission is unreliable and the
gaps are invisible to the person reconstructing it.

Distinguish, per the venue's categories: literature discovery and synthesis, theory
development, drafting, language editing, code generation, statistical analysis, figure
generation, and reproducibility checking. Record human verification for each. Any AI or
third-party model used *inside* the research pipeline needs model, version, validation, and
reproducible cached outputs — that is a methods disclosure, not a courtesy.

## The cover letter

Short, and a case rather than a summary. The editor is deciding whether to spend reviewers on
it. State what the paper changes for *this venue's* readership. See
`core/engineer-argument/references/genres.md` § *Journal cover letter*.

- [ ] Names the contribution as a change, not as an object.
- [ ] Says why this venue.
- [ ] Discloses related submissions, prior rejections where required, and any conflicted
      reviewers.
- [ ] Does not restate the abstract.

## Final pre-flight

- [ ] Every coauthor has seen the final version and approved submission.
- [ ] Author order and affiliations confirmed.
- [ ] Corresponding author contact details correct.
- [ ] The submitted file is the one you think it is. Open the PDF the portal generated and
      read it.
- [ ] `project/worklog.md` state block updated to stage 8, with the submission date.

## After acceptance

Stage 10, and not automatic.

- [ ] Proofs checked against the accepted manuscript, not against your latest local file.
- [ ] Numbers and symbols survived typesetting — subscripts, minus signs, Greek letters, and
      confidence intervals are the usual casualties.
- [ ] Repository links updated from private or embargoed to public, and verified live.
- [ ] Preprint updated or withdrawn per the venue's policy.
- [ ] `project/evidence-ledger.md` closed out: every claim at its final status.
- [ ] `project/worklog.md` state block set to stage 10, with what a future reader of this
      repository needs to know.
