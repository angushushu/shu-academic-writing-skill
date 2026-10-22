# shu-academic-writing-skill

This directory is a portable, self-contained skill bundle for developing and auditing an
empirical research manuscript.

**Read `README.md` first** for what it is and what it is measured to do, then `SKILL.md`. For the
benchmark results and the version-by-version evolution, read `BENCHMARK.md`; the full measurement
record is `EVIDENCE.md`.

`SKILL.md` is the router: it explains the two-layer structure (`core/` = generic method,
`project/` = this manuscript's facts), lists the modules, and gives the order of operations.

Before making any claim about a specific manuscript, read `project/project-profile.md`.

Nothing here depends on a plugin system, slash-command registry, or particular agent runtime.
Modules are plain Markdown; you invoke one by reading it. Scripts are stdlib-only Python 3.