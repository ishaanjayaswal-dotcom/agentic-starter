"""
summarise - turn long text into a short summary.

This skill NEEDS a real model. The kernel does not fake one.
Wire your key or local Ollama during the START-HERE interview,
then replace the body of run() so it actually calls your model.

Until then this skill returns a clear "not configured" result.
It never invents a summary.
"""


def run(payload):
    payload = payload or {}
    text = payload.get("text") or ""

    if not text.strip():
        return {"ok": False, "error": "text is required"}

    # Honest refusal. No canned paragraph. No pretend findings.
    return {
        "ok": False,
        "error": "no model configured",
        "hint": "Open START-HERE.md, finish the interview, then wire your model here.",
    }
