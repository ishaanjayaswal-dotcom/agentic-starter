# CLAUDE.md - briefing for coding agents on this repo

You are editing **agentic-starter**, a beginner-grade kernel for agentic systems.

## Read first

1. `START-HERE.md` - if the human has not done the interview yet, run that interview and write **no code** until answers exist.
2. `PATTERNS.md` - doctrine; do not invent architecture that fights these rules.
3. `README.md` - scope and non-goals.

## Layout (keep it)

- `router.py` - three tiers, print every decision, ASCII only in prints
- `orchestrator.py` - goal to skills to job record, max 3 workers
- `loop.py` - five stages; `verify()` is meant to be rewritten for real artifacts
- `skills/` - one module per skill, each exposes `run(payload) -> dict`
- `memory/` + `vault/` - notes as markdown with simple frontmatter and `links:`
- `tools/notes_server.py` - tiny discoverable tool surface
- `server.py` - `/health`, `/dispatch`, `/jobs`
- `smoke_test.py` - must stay zero-key green

## Non-negotiables

- **No mocks.** Never invent model output, research, findings, or summaries.
- Kernel path must run with **no API key**.
- **ASCII only** in `print()` strings (Windows cp1252).
- Every file must stay readable in one sitting. No frameworks for their own sake.
- Do not import or copy from any private OS outside this repo.

## After changes

```bash
python smoke_test.py
```

Fix until it prints that the kernel booted, routed a job, and wrote a note to the vault.

## When adding a skill

1. New file under `skills/` with docstring + `run`.
2. Teach `orchestrator.py` how to pick it from a goal (keywords).
3. Prefer real artifacts in `vault/` or files the human named.
4. If the skill needs a model, refuse clearly until the human wires one.
