"""
Orchestrator: one goal in, work back as a job record.

Picks skills from the goal text, runs them (at most three workers),
and returns a simple job dict. No watchers, no recovery ladder.
"""

import concurrent.futures

from router import route
from skills import list_skills, run_skill

# Cap fan-out so a beginner can still read the control flow.
MAX_WORKERS = 3

# Keyword -> skill name. First useful matches win, up to MAX_WORKERS.
GOAL_SKILLS = [
    (("write", "note", "save", "record"), "write_note"),
    (("search", "find", "look"), "search_notes"),
    (("summar", "tldr"), "summarise"),
]

# In-memory job log for the tiny HTTP server.
JOBS = []
_next_id = 1


def _pick_skills(goal):
    """Return up to MAX_WORKERS skill names for this goal."""
    text = (goal or "").lower()
    chosen = []
    for keywords, name in GOAL_SKILLS:
        if name in chosen:
            continue
        if any(k in text for k in keywords):
            chosen.append(name)
        if len(chosen) >= MAX_WORKERS:
            break
    # Default: write a note about the goal so the kernel always does something real.
    if not chosen:
        chosen = ["write_note"]
    return chosen


def _payload_for(skill_name, goal):
    """Build a beginner-grade payload from the goal string."""
    if skill_name == "write_note":
        return {
            "title": "Job note",
            "body": "Goal received by orchestrator:\n\n%s\n" % goal,
            "links": ["kernel"],
        }
    if skill_name == "search_notes":
        # Use the whole goal as the query; skill will still work.
        return {"query": goal}
    if skill_name == "summarise":
        return {"text": goal}
    return {"goal": goal}


def _run_one(skill_name, goal):
    payload = _payload_for(skill_name, goal)
    try:
        result = run_skill(skill_name, payload)
        return {"skill": skill_name, "ok": bool(result.get("ok", True)), "result": result}
    except Exception as exc:
        return {"skill": skill_name, "ok": False, "error": str(exc)}


def dispatch(goal):
    """
    Route the goal, run matching skills (fan-out <= 3), return a job record.
    """
    global _next_id

    decision = route(goal)
    skill_names = _pick_skills(goal)
    # Only run skills that actually exist in the folder.
    available = set(list_skills())
    skill_names = [s for s in skill_names if s in available] or ["write_note"]

    print("[orchestrator] skills=%s" % ", ".join(skill_names))

    results = []
    workers = min(MAX_WORKERS, len(skill_names))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_run_one, name, goal) for name in skill_names]
        for fut in concurrent.futures.as_completed(futures):
            results.append(fut.result())

    job = {
        "id": _next_id,
        "goal": goal,
        "tier": decision["tier"],
        "skills": skill_names,
        "results": results,
        "ok": all(r.get("ok") for r in results),
    }
    _next_id += 1
    JOBS.append(job)

    print("[orchestrator] job_id=%s ok=%s" % (job["id"], job["ok"]))
    return job


def get_job(job_id):
    for job in JOBS:
        if job["id"] == job_id:
            return job
    return None


def list_jobs():
    return list(JOBS)


if __name__ == "__main__":
    dispatch("write a note about the kernel boot")
