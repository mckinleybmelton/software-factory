---
description: Use when posting a completed PR review packet to a Jira ticket at pr_review without changing stage labels.
---

# Post review packet

Requires the Atlassian connector tools (see `account` MCP connection). If those tools are unavailable, return the review packet body and state that OAuth/auth is required — do **not** invent a successful post.

You **comment only**. You never set `done`, `implementation`, or `pr_review`. Product/human owns approve → `done` and reject → `implementation`.

## Procedure

1. Confirm the packet passes `review-pr/references/review-packet-contract.md`.
2. Read the ticket. Confirm current factory stage is already **`pr_review`**.
   - If it is **not**: **abort** — do **not** add a comment, do **not** change labels. Hand back `blocked_wrong_stage` with the **actual** stage. Stop here.
3. Confirm a PR URL is in the packet. If missing: abort `blocked_missing_pr` — no comment, no label change.
4. Add a comment with the rendered review packet markdown (`## PR review` … sections, including the PR link).
5. Do **not** change factory stage labels. Do not approve. Do not merge.

## Factory stage labels (do not write)

`prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`

## Reply after successful post

```text
Posted PR review packet to <KEY>
Stage unchanged: pr_review
PR: <url>
Handoff: orchestrator
Ticket: <KEY>
Stage: pr_review
Status: awaiting human PR review
```

## Reply when auth unavailable (after stage confirmed `pr_review`)

```text
PR review packet ready for <KEY> (not posted)
Stage: pr_review
Status: pr_review_ready_jira_auth_required
Handoff: orchestrator
Ticket: <KEY>
Stage: pr_review
Status: pr_review_ready_jira_auth_required
```

## Reply on abort

Do **not** add a Jira comment before aborting. No label changes.

```text
Aborted post to <KEY>
Reason: blocked_wrong_stage|blocked_missing_pr|blocked_missing_architecture|blocked_missing_acceptance_criteria
Handoff: orchestrator
Ticket: <KEY>
Stage: <actual stage on ticket, or unknown>
Status: blocked_wrong_stage|blocked_missing_pr|blocked_missing_architecture|blocked_missing_acceptance_criteria
```
