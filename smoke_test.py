"""
Zero-key smoke test for the KERNEL (not a brain, not a model).

Proves:
  1. router picks a tier and prints it
  2. orchestrator dispatches a real write_note skill
  3. a note lands in vault/
  4. search_notes can find it
  5. the five-stage loop can finish

No API key. No model. No fake research text.
ASCII only so Windows cp1252 consoles do not crash.
"""

import os
import sys
from pathlib import Path

# Run from repo root so imports resolve.
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    print("=== agentic-starter smoke test (kernel only) ===")
    print("")

    # 1. Router
    from router import route

    decision = route("write a note about smoke test")
    assert decision["tier"] in ("deep", "normal", "cheap"), "bad tier"
    print("[ok] router returned tier=%s" % decision["tier"])

    # 2. Dispatch -> write_note
    from orchestrator import dispatch

    job = dispatch("write a note about smoke test boot")
    assert job.get("ok"), "dispatch job failed: %r" % (job,)
    print("[ok] orchestrator job_id=%s" % job["id"])

    # 3. Find the note path from results
    note_path = None
    for item in job.get("results") or []:
        result = item.get("result") or {}
        if result.get("path"):
            note_path = result["path"]
            break
    assert note_path, "write_note did not return a path"
    full = ROOT / note_path
    assert full.is_file(), "note file missing: %s" % note_path
    text = full.read_text(encoding="utf-8")
    assert "smoke test" in text.lower() or "goal received" in text.lower()
    print("[ok] vault note written: %s" % note_path)

    # 4. search_notes skill
    from skills import run_skill

    search = run_skill("search_notes", {"query": "kernel"})
    assert search.get("ok"), "search_notes failed"
    assert search.get("count", 0) >= 1, "search_notes found nothing"
    print("[ok] search_notes hits=%s" % search["count"])

    # 5. summarise must refuse honestly (no fake summary)
    summary = run_skill("summarise", {"text": "hello world"})
    assert summary.get("ok") is False, "summarise must not pretend"
    assert "model" in (summary.get("error") or "").lower()
    print("[ok] summarise correctly refused without a model")

    # 6. loop finishes
    from loop import run_loop

    loop_result = run_loop("write a note that the loop finished", max_steps=3)
    assert loop_result.get("ok"), "loop did not verify"
    print("[ok] loop verified done")

    # 7. tools surface
    from tools.notes_server import call_tool, list_tools

    tools = list_tools()
    assert any(t["name"] == "write_note" for t in tools)
    tool_result = call_tool(
        "write_note",
        {"title": "Tool surface check", "body": "Written via tools/notes_server.", "links": ["kernel"]},
    )
    assert tool_result.get("ok") and tool_result.get("path")
    print("[ok] notes_server tool wrote %s" % tool_result["path"])

    print("")
    print("Your kernel booted, routed a job, and wrote a note to your vault.")
    print("No model was called. No API key was used. That is correct.")
    print("Next: open START-HERE.md and paste it into Claude Code or Codex.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print("")
        print("SMOKE FAILED: %s" % exc)
        sys.exit(1)
    except Exception as exc:
        print("")
        print("SMOKE FAILED: %s" % exc)
        sys.exit(1)
