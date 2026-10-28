---
description: Use when posting a completed design artifact to a Jira ticket and moving the stage to design_review.
---

# Post design to Jira

Requires the Atlassian connector tools (see `account` MCP connection). If those tools are unavailable, return the design body and state that OAuth/auth is required — do not invent a successful post.

You are the **only** writer of `design_review`. You never set `design_draft` (product/human owns that label before you run).

## Procedure

1. Confirm the design passes `draft-design/references/design-contract.md`.
2. Read the ticket (key from the orchestrator message). Confirm current factory stage is already **`design_draft`**. If it is not (missing, still `prd_review`, already `design_review`, or another stage), **do not** change labels; hand back with the draft in the reply and say product/human must set `design_draft` first.
3. Confirm a PRD is present (comment or description); if missing, say so and still hand back with the draft in the reply (do not advance labels without a PRD unless the orchestrator explicitly said the PRD is in the message only and Jira lacks it — still do not invent `design_draft`).
4. Add a comment with the rendered design markdown (`## Design` … sections).
5. Update factory stage labels **only** in this transition:
   - Remove `design_draft` (and any other factory stage labels listed below).
   - Add `design_review`.
   - Do **not** add or re-apply `design_draft`.
6. Do **not** transition beyond `design_review`. Do not approve.

## Factory stage labels

`prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`

Keep exactly one of these on the ticket after your update.

## Reply after post

```text
Posted design to <KEY>
Labels: design_review
Handoff: orchestrator — awaiting human design review
```
