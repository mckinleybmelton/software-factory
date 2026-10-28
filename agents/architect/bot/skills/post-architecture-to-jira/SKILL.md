---
description: Use when posting a completed architecture to Jira and advancing the ticket to architecture_review.
---

# Post architecture to Jira

Requires the Atlassian connector tools (see `account` MCP connection). If those tools are unavailable, return the architecture body and state that OAuth/auth is required — do **not** invent a successful post, do **not** claim `Labels: architecture_review` or `Stage: architecture_review`.

You are the **only** writer of `architecture_review`. You never set `architecture_draft` (product/human owns that label before you run).

## Procedure

1. Confirm the architecture passes `draft-architecture/references/architecture-contract.md` (including a **dependency graph**).
2. Read the ticket (key from the orchestrator message). Confirm current factory stage is already **`architecture_draft`**.
   - If it is **not** (missing, still `design_review`, already `architecture_review`, or another stage): **abort** — do **not** add a comment, do **not** change labels, do **not** claim `architecture_review`. Hand back with status `blocked_wrong_stage` and the **actual** stage found. Do **not** instruct applying `architecture_draft` (that can skip `design_review` or rewind a later stage). Orchestrator must re-route from the real stage. Stop here.
3. Confirm a PRD and design are present (comments or description, or supplied in the orchestrator message). If PRD missing: **abort** — no comment, no label change; hand back with status `blocked_missing_prd` and the current stage (`architecture_draft`). If design missing: same with `blocked_missing_design`. Stop here.
4. Add a comment with the rendered architecture markdown (`## Architecture` … sections, including the dependency graph).
5. Update factory stage labels **only** in this transition:
   - Remove `architecture_draft` (and any other factory stage labels listed below).
   - Add `architecture_review`.
   - Do **not** add or re-apply `architecture_draft`.
6. Do **not** transition beyond `architecture_review`. Do not approve.

## Factory stage labels

`prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`

Keep exactly one of these on the ticket after a successful update.

## Reply after successful post

```text
Posted architecture to <KEY>
Labels: architecture_review
Handoff: orchestrator
Ticket: <KEY>
Stage: architecture_review
Status: awaiting human architecture review
```

## Reply when auth unavailable (after stage confirmed `architecture_draft`)

```text
Architecture draft ready for <KEY> (not posted)
Stage: architecture_draft
Status: architecture_ready_jira_auth_required
Handoff: orchestrator
Ticket: <KEY>
Stage: architecture_draft
Status: architecture_ready_jira_auth_required
```

## Reply on abort (wrong stage / missing PRD or design)

Do **not** add a Jira comment before aborting. Stop the procedure; no label changes.

```text
Aborted post to <KEY>
Reason: blocked_wrong_stage|blocked_missing_prd|blocked_missing_design
Handoff: orchestrator
Ticket: <KEY>
Stage: <actual stage on ticket, or unknown>
Status: blocked_wrong_stage|blocked_missing_prd|blocked_missing_design
```
