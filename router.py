"""
Three-tier model router.

Prints every decision. With no model wired, it still picks a tier
and says plainly that nothing will call a model yet.
"""

# Rules are checked top to bottom. First match wins.
# deep  = hard thinking, design, multi-step planning
# cheap = tiny lookups, status, formatting
# normal = everything else

RULES = [
    ("deep", ("design", "architect", "plan", "debug", "complex", "refactor")),
    ("cheap", ("list", "status", "health", "format", "rename", "count")),
    ("normal", ()),  # fallback, always matches
]

# Set this later (via START-HERE interview) to a real client if you want.
# The kernel never requires it.
MODEL = None


def pick_tier(goal):
    """Return 'deep', 'normal', or 'cheap' from a short goal string."""
    text = (goal or "").lower()
    for tier, keywords in RULES:
        if not keywords:
            return tier
        for word in keywords:
            if word in text:
                return tier
    return "normal"


def route(goal):
    """
    Decide a tier for this goal and print the decision.

    Returns a dict: {goal, tier, model_ready, message}
    Does NOT call a model. Routing is the lesson.
    """
    tier = pick_tier(goal)
    model_ready = MODEL is not None

    if model_ready:
        message = "model is configured; caller may use it for this tier"
    else:
        message = "no model configured; kernel will still run skills that need none"

    # ASCII only - Windows consoles (cp1252) crash on fancy arrows.
    print("[router] goal=%r" % (goal,))
    print("[router] tier=%s" % tier)
    print("[router] %s" % message)

    return {
        "goal": goal,
        "tier": tier,
        "model_ready": model_ready,
        "message": message,
    }


if __name__ == "__main__":
    for sample in (
        "design a note layout",
        "list notes in the vault",
        "write a short weekly update",
    ):
        route(sample)
        print("")
