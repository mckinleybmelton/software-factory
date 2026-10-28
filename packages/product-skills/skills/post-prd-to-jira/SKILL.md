---
description: Use when posting a completed PRD to Jira and advancing the ticket to prd_review.
---

# Post PRD to Jira

Requires the Atlassian connector tools (see `account` MCP connection). If those tools are unavailable, return the PRD body and state that OAuth/auth is required — do not invent a successful post.

## Procedure

1. Confirm the PRD passes the contract in skill `productSkills__draft-prd` (`references/prd-contract.md` under that skill).
2. Read the ticket (key from the orchestrator message).
3. Add a comment with the rendered PRD markdown (`## PRD` … sections).
4. Update factory stage labels:
   - Remove `prd_draft` (and any other factory stage labels listed below).
   - Add `prd_review`.
5. Do **not** transition beyond `prd_review`. Do not approve.

## Factory stage labels

`prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`

Keep exactly one of these on the ticket after your update.

## Reply after post

```text
Posted PRD to <KEY>
Labels: prd_review
Handoff: orchestrator — awaiting human PRD review
```
