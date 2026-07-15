# agentic-starter

A small, readable kernel that teaches five agentic layers, plus a prompt that makes **your** coding agent interview you and shape the OS around your work.

No API key required for the kernel path. Nothing pretends to be a model.

## First 30 minutes

1. **Install [Claude Code](https://claude.com/claude-code)** (or use Codex / Cursor — any coding
   agent works, the repo does not assume a specific one).
2. **Clone this repo:**
   ```bash
   git clone https://github.com/<your-username>/agentic-starter.git
   cd agentic-starter
   ```
3. **Run the first command** (proves the kernel with zero setup, zero API key):
   ```bash
   python smoke_test.py
   ```
4. Open [`START-HERE.md`](START-HERE.md) and paste it into your coding agent to shape the kernel
   around your own work.

## 60-second path

```bash
python smoke_test.py
```

You should see a line like:

```text
Your kernel booted, routed a job, and wrote a note to your vault.
```

That proves routing, dispatch, skills, memory, and vault write. It does **not** call an LLM.

## Then make it yours

1. Open [`START-HERE.md`](START-HERE.md).
2. Paste the block into Claude Code, Codex, or Cursor.
3. Answer the interview. **No code until you have answers.**
4. Let the agent build **one** real skill for your actual task.

If the interview does not happen, this repo failed you even if tests are green.

## What is in here

| Path | Role |
|------|------|
| `router.py` | Three tiers: deep / normal / cheap. Prints every decision. |
| `orchestrator.py` | Goal -> skills -> up to 3 workers -> job record |
| `loop.py` | observe / plan / execute / verify / improve |
| `skills/` | One file per skill; folder-scan registry |
| `memory/` | File store + vault writer (`raw` -> note) |
| `vault/` | Where notes land |
| `tools/notes_server.py` | One small MCP-style tool surface |
| `server.py` | `GET /health`, `POST /dispatch`, `GET /jobs` |
| `smoke_test.py` | Zero-key green line |
| `PATTERNS.md` | Doctrine: rule, failure, what to do instead |
| `CLAUDE.md` | How to brief a coding agent on this repo |

## Optional HTTP server

```bash
python server.py
```

Then `GET http://127.0.0.1:8765/health`.

## Codespaces / dev container

Open in GitHub Codespaces or any environment that reads `.devcontainer/`. Smoke test is the same command.

## What this is not

- Not a hosted product
- Not a copy of anyone's private production OS
- Not a fake brain with canned "findings"
- Not a framework

Skills that need a model (`summarise`) say so and point you at `START-HERE.md`. Skills that do not (`write_note`, `search_notes`) simply work.

## Requirements

- Python 3.10+ recommended
- Stdlib only for the kernel
