---
description: Use when asked what is in flight, what to start next, to triage the board, or to move stuck or mislabeled tickets.
---

# Manage backlog

Triage the configured Jira project (or a named filter/board) into delivery buckets, summarize, and propose next steps. Transition or relabel tickets **only** when the user explicitly asks or states a clear rule.

Requires Atlassian connector tools (`account` MCP). If tools are missing or unauthorized, say so and list what you would query — do not invent board contents.

## Config

Read `references/status-buckets.md` for project/filter resolution, status → bucket map, factory stage labels, and stale thresholds. Prefer env overrides when set; otherwise use the reference defaults.

## Procedure

1. **Resolve scope**
   - Project key from `JIRA_PROJECT_KEY` / `FACTORY_JIRA_PROJECT`, or the key named in the ask.
   - Optional named filter / board from the ask or `JIRA_FILTER_ID` / `JIRA_BOARD_ID`.
   - If scope is unclear and env is unset, ask once for project key (or filter/board), then continue.

2. **Pull open issues**
   - Query open (non-done unless the user asked for finished too) issues for that project/filter/board via Atlassian MCP.
   - Include: key, summary/title, status, labels, assignee, updated/created, and any blocker flags or linked blockers when available.
   - Cap noise: prefer active + recently updated; if the board is huge, summarize counts and sample the oldest/stale items per bucket unless the user wants a full dump.

3. **Bucket**
   - Map each issue's Jira status into one of: `yet_to_start`, `in_progress`, `in_review`, `finished` using the status map in `references/status-buckets.md` (env overrides win).
   - Note the factory stage label if present (exactly one of the factory stage labels).
   - Treat unknown statuses as `in_progress` and call them out under assumptions.

4. **Summarize each bucket**
   For every issue line include:
   - Key and title
   - Factory stage label (or `none`)
   - Blockers (flag, linked blocked-by, or explicit comment cues) when present
   - Age: days since last update (and created age if never updated meaningfully)

5. **Propose next steps** (always; do not execute moves here)
   - **Start:** highest-value yet-to-start items that are unblocked, have a clear factory stage (often `prd_draft` or the next draft stage), and do **not** have a `*_review` factory stage label (`prd_review`, `design_review`, `architecture_review`, `pr_review`). Review-gated tickets belong only under Human gate.
   - **Unblock:** in-progress / in-review items with blockers or missing owners.
   - **Human gate:** anything on a `*_review` factory stage — waiting on human approve/reject; do not approve. Never also list these under Start, even if status is `yet_to_start` and unblocked.
   - **Stale:** past the stale threshold in the reference (default: no update in 7+ days while open).

6. **Move / transition only when authorized**
   - Default: **read + propose only**. Never silently reshuffle priority, rank, or status.
   - Transition, comment, or update labels **only** when:
     - the user explicitly asks to move/update specific tickets, or
     - the user stated an explicit rule this turn (e.g. "mark review stale after 7 days", "on changes_requested return to draft").
   - Safe examples when asked: mark stale review, advance stage label after gate approval (hand orchestrator the run), return to draft on `changes_requested`.
   - Never approve a gate yourself. Never set stage past what the human authorized.

7. **Handoff for factory runs**
   - If a ticket needs a factory stage **run** (draft/implementation work), hand off to the **orchestrator** with ticket key and stage. Do not open branches, rewrite PRDs, or call design/architect/implementer/reviewer yourself.

## Output shape

```markdown
## Backlog triage (<project or filter>)

### Yet to start
- KEY — title — stage: … — blockers: … — age: Nd

### In progress
- …

### In review
- …

### Finished
- … (omit or keep short unless asked)

### Next steps
- Start: …
- Unblock: …
- Waiting on human gate: …
- Stale: …

### Moves (only if authorized)
- … or "none — proposal only"
```

If Jira was unavailable:

```text
Backlog triage skipped: Atlassian/Jira auth required.
Scope intended: <project/filter>
Handoff: orchestrator (no board changes)
```
