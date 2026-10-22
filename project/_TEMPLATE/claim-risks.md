# Claim risks

> **TEMPLATE — FILL THIS IN.** Project-specific phrasings that must be caught before
> submission. Read by `core/audit-manuscript/` and by `scripts/audit_draft.py --patterns`.

## Machine-checkable patterns

`scripts/audit_draft.py` parses the block below. One rule per line, `label :: regex`.
Regexes are case-insensitive Python syntax. These run *in addition to* the script's
built-in generic patterns, so add only what is specific to this project.

```patterns
example claim to catch :: \b(some|specific)\s+phrase\b
```

## Automatic blocker candidates for this project

<!-- Generic blockers live in core/audit-manuscript/references/editorial-rubric.md.
     List here only the ones peculiar to this manuscript's evidence situation. -->

-

## Banned formulations

<!-- Exact sentences from earlier drafts that overstate the evidence, with the reason.
     Being concrete here is what makes this file useful a year from now. -->

| Formulation | Why it fails | Say instead |
|---|---|---|
| | | |
