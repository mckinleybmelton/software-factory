---
description: Use when opening the product-repo PR for a completed implementation and moving the stage to pr_review only after the PR exists.
---

# Open PR

Requires GitHub tools (account `github` MCP connector and/or authenticated `gh`) and Atlassian tools for the Jira PR-link comment + `pr_review` label. Prefer GitHub MCP; fall back to `gh` when MCP is unavailable.

You are the **only** writer of `pr_review`. You never set `implementation` (product/human owns that label before you run). Set `pr_review` **only after** a real PR URL exists.

## Procedure

1. Confirm `implement-change` produced a pushed ticket branch with code + tests (or equivalent ready-to-review commits).
2. Read the ticket. Confirm current factory stage is already **`implementation`**.
   - If it is **not**: **abort** — do **not** open a PR, do **not** add a Jira comment, do **not** change labels, do **not** claim `pr_review`. Hand back `blocked_wrong_stage` with the **actual** stage. Stop here.
3. Confirm approved architecture and acceptance criteria are present (orchestrator message and/or Jira). If architecture missing: abort `blocked_missing_architecture` (no PR, no label). If acceptance criteria missing: abort `blocked_missing_acceptance_criteria`. Stop here.
4. Open **one** pull request against the product default branch (`FACTORY_PRODUCT_DEFAULT_BRANCH` / `main`):
   - Title references the ticket key.
   - Body includes summary, acceptance-criteria coverage, test notes, and links to approved architecture.
   - Do **not** merge. Do **not** request self-approval as final.
5. **Only after** the PR URL exists: add a Jira comment with the PR link (and short implementation summary).
6. Update factory stage labels **only** in this transition (and only after steps 4–5 succeeded):
   - Remove `implementation` (and any other factory stage labels listed below).
   - Add `pr_review`.
   - Do **not** add or re-apply `implementation`.
7. Do **not** transition beyond `pr_review`. Do not approve. Do not merge.

## Factory stage labels

`prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`

Keep exactly one of these on the ticket after a successful update.

## Race safety

- Never set `pr_review` before the PR exists (avoids the orchestrator asking reviewer against a missing PR).
- Never claim `Labels: pr_review` / `Stage: pr_review` if the PR open or Jira update failed.
- If GitHub succeeds but Jira auth fails: leave stage at `implementation`, report the PR URL, and use `implementation_ready_jira_auth_required` so product/human can comment + label after the PR is real — do **not** invent `pr_review`.

## Reply after successful post

```text
Opened PR <url> for <KEY>
Posted PR link to <KEY>
Labels: pr_review
Handoff: orchestrator
Ticket: <KEY>
Stage: pr_review
PR: <url>
Status: awaiting human PR review
```

## Reply when auth unavailable (after stage confirmed `implementation`)

```text
Implementation ready for <KEY> (PR and/or Jira not fully updated)
Stage: implementation
Status: implementation_ready_github_auth_required|implementation_ready_jira_auth_required|implementation_ready_auth_required
PR: <url or none>
Handoff: orchestrator
Ticket: <KEY>
Stage: implementation
Status: implementation_ready_github_auth_required|implementation_ready_jira_auth_required|implementation_ready_auth_required
```

## Reply on abort (wrong stage / missing inputs)

Do **not** open a PR or add a Jira comment before aborting. Stop; no label changes.

```text
Aborted open-pr for <KEY>
Reason: blocked_wrong_stage|blocked_missing_architecture|blocked_missing_acceptance_criteria|blocked_missing_product_repo
Handoff: orchestrator
Ticket: <KEY>
Stage: <actual stage on ticket, or unknown>
Status: blocked_wrong_stage|blocked_missing_architecture|blocked_missing_acceptance_criteria|blocked_missing_product_repo
```
