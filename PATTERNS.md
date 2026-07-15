# Patterns (doctrine)

Short rules. Each one paid for a real failure. Nobody's private system is named here.
Use these when you extend this starter.

---

## Memory is a pipeline, not a pile

**Rule:** Raw input becomes a note through clear stages. Do not dump chat logs into a folder and call it memory.

**Failure:** A directory of unsorted exports grows until search is useless and nobody trusts what is in there.

**Instead:** Keep a short path (this repo: raw fields -> markdown note with `links:`). Add stages only when you can say what each stage fixes.

---

## One writer per file, always

**Rule:** Only one process or agent may write a given file at a time.

**Failure:** Two writers interleave updates; the file ends truncated, half-merged, or silently last-write-wins without anyone noticing.

**Instead:** Serialize writes. One owner per path. If two jobs need the same note, queue them or write separate notes and link them.

---

## Verify, never trust the report

**Rule:** A report is a claim. The artifact is the truth.

**Failure:** A job returns `ok: true` while the note was never written, the row never updated, or the test never ran.

**Instead:** `verify()` checks the artifact (file on disk, HTTP status, row count). Rewrite the naive verifier in `loop.py` for your real done-condition.

---

## Audit with a different model than the one that built it

**Rule:** The builder does not grade its own homework.

**Failure:** The same model that shipped a bug also "reviews" the diff and waves it through.

**Instead:** Use a second model or a human for audit. Even a cheap second pass catches "I forgot to call the function" mistakes the builder papered over in prose.

---

## Dry-run until proven, then and only then let it write

**Rule:** New automations start read-only. Writes are a privilege you turn on after a green dry-run.

**Failure:** A half-finished skill renames files, sends mail, or overwrites notes on the first try.

**Instead:** Print what you *would* write. Diff it. When it is boringly correct three times, enable the write path.

---

## Watch the artifact, not the messenger

**Rule:** Judge success by the output that lives after the process exits, not by a chatty status line.

**Failure:** A worker says "done" and then dies before flush; dashboards stay green; the vault is empty.

**Instead:** Poll or open the note, file, or URL. Heartbeats are optional. Artifacts are mandatory.

---

## A gate you cannot see into is a gate that lies

**Rule:** Every check should print or log what it checked and what it saw.

**Failure:** A silent "permission ok" or "tests passed" gate fails closed or open with no trail, and you debug ghosts.

**Instead:** Make gates loud and boring: inputs, threshold, measured value, pass/fail. The router in this repo prints every decision for that reason.

---

## If a spec bans every technique that makes work good, it will get bad work

**Rule:** Constraints should stop harm, not stop craft.

**Failure:** A brief bans structure, tools, iteration, and judgment, then blames the model for shallow output.

**Instead:** Ban the few things that are actually dangerous (secrets, prod writes, out-of-scope systems). Leave room for reading, checking, and rewriting until the artifact is right.
