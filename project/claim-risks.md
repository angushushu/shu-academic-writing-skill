# Claim risks

## Machine-checkable patterns

`scripts/audit_draft.py` parses the block below. One rule per line, `label :: regex`.
Regexes are case-insensitive Python syntax. These run *in addition to* the script's
built-in generic patterns, so add only what is specific to this project.

```patterns
example claim to catch :: \b(some|specific)\s+phrase\b
```

## Automatic blocker candidates for this project

-

## Banned formulations

| Formulation | Why it fails | Say instead |
|---|---|---|
| | | |
