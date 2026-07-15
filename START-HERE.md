# START HERE

Paste **everything below the line** into Claude Code, Codex, or Cursor.
Do not skip the interview. The interview is the product.

---

You are helping me turn this `agentic-starter` repo into **my** small agentic OS.

## Hard rules for you (the coding agent)

1. **Interview me first. Write no code until I have answered.**
2. Ask the five questions below, one block at a time if you like, but get real answers.
3. After answers, build **depth not breadth**: fully implement **ONE** working skill that does a real task from my answers. Do not scaffold five empty stubs.
4. Keep the existing kernel: `router.py`, `orchestrator.py`, `loop.py`, `memory/`, `skills/` folder scan, `vault/`, `smoke_test.py`.
5. **No mocks.** Never invent research, findings, summaries, or model output. If a skill needs a model and none is wired, refuse honestly.
6. Keep every file beginner-readable. Small files, plain names, stdlib only unless I already use something else.
7. **ASCII only** in anything that `print()`s (Windows consoles often crash on fancy unicode).
8. After you build, run `python smoke_test.py` and fix until green.
9. My first vault note must be the **interview transcript** (real answers I gave you).

## Interview questions (ask me these before any code)

1. What work actually eats my week? Name three real tasks.
2. Which tools do I already live in? (files, notes app, calendar, mail, code, chat)
3. What must this system **never** touch? Name it now, out loud.
4. What does "done" look like for task one? How would a machine **prove** it (file exists, row changed, URL returns 200)?
5. What should happen while I sleep, if anything?

## After I answer, do this in order

### A. Write the interview into the vault
- Create `vault/interview-transcript.md` with frontmatter (`title`, `created`, `links`) and my full answers.
- This is real memory, not a sample.

### B. Build ONE skill end to end
- Add `skills/<my_skill>.py` with a short docstring and `run(payload) -> dict`.
- Wire it so `orchestrator.py` can pick it from goals that match my task one.
- If the skill needs a model: wire **my** key or **my** local Ollama only if I provide that. Otherwise keep model-free parts working and refuse model steps honestly.
- Update `loop.py` `verify()` so "done" checks the **artifact** I described in question 4, not just a success flag.

### C. Shape routing and agent brief to me
- Adjust `router.py` RULES keywords so deep/normal/cheap match how I talk about my work.
- Write or update `CLAUDE.md` so a future coding agent knows **my** constraints from question 3.

### D. Prove it
- Run: `python smoke_test.py`
- Then run one real dispatch for my task (CLI or a few lines of Python) and show me the vault/artifact output.
- Tell me in plain language what was kernel (no model) vs what needed a model.

## What this repo already is

Five thin layers you can read in one sitting:

| Layer | File(s) | Lesson |
|-------|---------|--------|
| Routing | `router.py` | Do not send everything to the biggest model |
| Skills | `skills/` | Agents discover tools; they do not memorise them |
| Orchestration | `orchestrator.py` | One brief in, work back |
| Memory | `memory/`, `vault/` | Memory is a pipeline, not a pile |
| Loop | `loop.py` | Run until you can prove you are done |

Read `PATTERNS.md` before you invent clever architecture. Those rules exist because the clever versions fail.

## What you must not do

- Do not copy anyone else's private OS, agent names, ports, or vault content.
- Do not add frameworks "for production".
- Do not label output research/findings/summary unless a real model produced it.
- Do not claim the smoke test "calls an LLM". It proves the kernel only.

Start now by asking me question 1.
