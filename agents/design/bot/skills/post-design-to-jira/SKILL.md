---
description: Use when posting a completed design artifact to a Jira ticket and moving the stage to design_review.
---

# Post design to Jira

Requires the Atlassian connector tools (see `account` MCP connection). If those tools are unavailable, return the design body and state that OAuth/auth is required — do **not** invent a successful post, do **not** claim `Labels: design_review` or `Stage: design_review`.

You are the **only** writer of `design_review`. You never set `design_draft` (product/human owns that label before you run).

## Procedure

1. Confirm the design passes `draft-design/references/design-contract.md`.
2. Read the ticket (key from the orchestrator message). Confirm current factory stage is already **`design_draft`**.
   - If it is **not** (missing, still `prd_review`, already `design_review`, or another stage): **abort** — do **not** add a comment, do **not** change labels, do **not** claim `design_review`. Hand back with status `blocked_wrong_stage` and the **actual** stage found. Do **not** instruct applying `design_draft` (that can skip `prd_review` or rewind a later stage). Orchestrator must re-route from the real stage. Stop here.
3. Confirm a PRD is present (comment or description). If missing and the orchestrator did not supply the approved PRD in the message: **abort** — no comment, no label change; hand back with status `blocked_missing_prd` and the current stage (`design_draft`). Stop here.
4. Add a comment with the rendered design markdown (`## Design` … sections).
5. Update factory stage labels **only** in this transition:
   - Remove `design_draft` (and any other factory stage labels listed below).
   - Add `design_review`.
   - Do **not** add or re-apply `design_draft`.
6. Do **not** transition beyond `design_review`. Do not approve.

## Factory stage labels

`prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`

Keep exactly one of these on the ticket after a successful update.

## Reply after successful post

```text
Posted design to <KEY>
Labels: design_review
Handoff: orchestrator
Ticket: <KEY>
Stage: design_review
Status: awaiting human design review
```

## Reply when auth unavailable (after stage confirmed `design_draft`)

```text
Design draft ready for <KEY> (not posted)
Stage: design_draft
Status: design_ready_jira_auth_required
Handoff: orchestrator
Ticket: <KEY>
Stage: design_draft
Status: design_ready_jira_auth_required
```

## Reply on abort (wrong stage / missing PRD)

Do **not** add a Jira comment before aborting. Stop the procedure; no label changes.

```text
Aborted post to <KEY>
Reason: blocked_wrong_stage|blocked_missing_prd
Handoff: orchestrator
Ticket: <KEY>
Stage: <actual stage on ticket, or unknown>
Status: blocked_wrong_stage|blocked_missing_prd
```
