"""
The five-stage loop: observe / plan / execute / verify / improve.

Ships deliberately naive. You are meant to rewrite verify() so "done"
matches your real work. It runs until verify says stop, or max_steps.
"""

from orchestrator import dispatch


def observe(goal, history):
    """What do we know right now?"""
    return {
        "goal": goal,
        "steps_so_far": len(history),
        "last_ok": history[-1]["ok"] if history else None,
    }


def plan(observation):
    """Decide the next small action. Beginner default: dispatch the goal."""
    return {
        "action": "dispatch",
        "goal": observation["goal"],
    }


def execute(step_plan):
    """Run one planned action. Only 'dispatch' is wired today."""
    if step_plan.get("action") == "dispatch":
        job = dispatch(step_plan["goal"])
        return {"ok": job.get("ok", False), "job": job}
    return {"ok": False, "error": "unknown action"}


def verify(goal, result):
    """
    Prove we are done.

    Naive on purpose: if the last execute reported ok, we stop.
    Rewrite this so it checks a real artifact (a file, a row, a URL).
    A report is a claim; the artifact is the truth.
    """
    if not result:
        return False
    return bool(result.get("ok"))


def improve(goal, result, history):
    """
    Adjust the goal slightly after a failed step.
    Naive: append a hint. Replace with real repair logic later.
    """
    if result and result.get("ok"):
        return goal
    return goal + " (retry with write_note)"


def run_loop(goal, max_steps=3):
    """
    Run observe -> plan -> execute -> verify -> improve until done or max_steps.

    Returns a dict with history and whether verify passed.
    """
    history = []
    current_goal = goal

    print("[loop] start goal=%r" % (goal,))

    for step in range(1, max_steps + 1):
        print("[loop] step=%s" % step)
        obs = observe(current_goal, history)
        step_plan = plan(obs)
        result = execute(step_plan)
        history.append(
            {
                "step": step,
                "plan": step_plan,
                "result": result,
                "ok": bool(result.get("ok")),
            }
        )
        if verify(current_goal, result):
            print("[loop] verified done at step %s" % step)
            return {"ok": True, "history": history, "goal": current_goal}
        current_goal = improve(current_goal, result, history)

    print("[loop] stopped at max_steps without verify")
    return {"ok": False, "history": history, "goal": current_goal}


if __name__ == "__main__":
    run_loop("write a note that the loop ran")
