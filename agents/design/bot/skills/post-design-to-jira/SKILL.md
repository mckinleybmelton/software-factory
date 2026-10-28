---
description: Use when posting a completed design artifact to a Jira ticket and moving the stage to design_review.
---

# Post design to Jira

Requires the Atlassian connector tools (see `account` MCP connection). If those tools are unavailable, return the design body and state that OAuth/auth is required — do not invent a successful post.

## Procedure

1. Confirm the design passes `draft-design/references/design-contract.md`.
2. Read the ticket (key from the orchestrator message). Confirm a PRD is present (comment or description); if missing, say so and still hand back with the draft in the reply.
3. Add a comment with the rendered design markdown (`## Design` … sections).
4. Update factory stage labels:
   - Remove `design_draft` (and any other factory stage labels listed below).
   - Add `design_review`.
5. Do **not** transition beyond `design_review`. Do not approve.

## Factory stage labels

`prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`

Keep exactly one of these on the ticket after your update.

## Reply after post

```text
Posted design to <KEY>
Labels: design_review
Handoff: orchestrator — awaiting human design review
```
