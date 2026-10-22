# Module map — how the modules reach each other

Every module is read on its own; agents arrive from a path, a search, or a prompt that names one
file. This map exists so that **no module is a dead end** and so the adversarial gate is reachable
from wherever you entered.

Measured problem this fixes: `core/engineer-argument/` and `core/polish-prose/` pointed at each
other and never at `core/audit-manuscript/`, and `core/corpus-metrics/` pointed at nothing. An
agent entering through prose work could not reach the audit at all.

```
                    ┌──────────────────────────┐
                    │  core/develop-manuscript │  plan, draft, restructure
                    └────────────┬─────────────┘
                                 │ step 8: revise in order
                    ┌────────────▼─────────────┐
                    │  core/engineer-argument  │  does it matter to these readers
                    └────────────┬─────────────┘
                                 │ argument settled?
                    ┌────────────▼─────────────┐
                    │  core/polish-prose       │  sentences only
                    └────────────┬─────────────┘
                                 │
        ┌────────────────────────▼─────────────────────────┐
        │  core/audit-manuscript    ADVERSARIAL GATE       │
        │  Read before submitting, and before declaring    │
        │  any draft submission-ready. Every other module  │
        │  can be skipped; this one is the last thing that │
        │  should be.                                      │
        └────────────────────────┬─────────────────────────┘
                                 │ a decision letter arrives
                    ┌────────────▼─────────────┐
                    │  core/respond-to-reviewers│  triage, response letter
                    └──────────────────────────┘

  side roads, reachable from anywhere:
    core/corpus-metrics   only when the question is textual measurement of a finished draft
    project/              the facts of THIS manuscript; read before any claim about its content
```

## If you arrived at a module directly

You may have been handed one file and never seen `SKILL.md`. Then:

1. **Read `project/project-profile.md`.** It holds this manuscript's facts. If it still contains
   template placeholders, say so and ask the author — do not invent project facts.
2. **Do the job the module describes**, and do not stray into another module's job. The table in
   `SKILL.md` says which job belongs to which file.
3. **Before declaring anything submission-ready, read `core/audit-manuscript/SKILL.md`.** This is
   the one hop that is not optional. A draft can be well-argued and well-written and still fail an
   adversarial gate, and the gate examines things the other modules never look at.

## What each module is *not* for

Saying this here means a module does not have to repeat it, and an agent that reads only one file
still learns where its file stops.

| Module | Not for |
|---|---|
| `develop-manuscript` | isolated sentence polishing; an independent adversarial audit |
| `engineer-argument` | copyediting; sentence-level style |
| `polish-prose` | repairing an unstable argument — fix the argument first |
| `audit-manuscript` | drafting; resolving an evidence conflict in the author's favor |
| `respond-to-reviewers` | the pre-submission audit — that is a different job |
| `corpus-metrics` | anything about whether the argument is right |

| `core/problem-framing/SKILL.md` | name what the reader believes, show why it fails, make the reader's work small | the operational machinery behind reader-layer move 1 |
| `core/reader-layer/SKILL.md` | one argument, one stake, no interruptions; reader surface vs record surface | the most validated module (29-7 and 11-1 against the comparison skill) |
