---
description: Use when opening a product-repo PR for an implementation ticket, or completing Jira comment + pr_review for an existing PR after auth recovery.
---

# Open PR

Requires GitHub tools (account `github` MCP connector and/or authenticated `gh`) and Atlassian tools for the Jira PR-link comment + `pr_review` label. Prefer GitHub MCP; fall back to `gh` when MCP is unavailable.

You are the **only** writer of `pr_review`. Product must never set `pr_review`. You never set `implementation` (product/human owns that label before you run). Set `pr_review` **only after** a real PR URL exists.

## Procedure

1. Confirm current factory stage is already **`implementation`**.
   - If it is **not**: **abort** — do **not** open a PR, do **not** add a Jira comment, do **not** change labels, do **not** claim `pr_review`. Hand back `blocked_wrong_stage` with the **actual** stage. Stop here.
2. Confirm approved architecture and acceptance criteria are present (orchestrator message and/or Jira). If architecture missing: abort `blocked_missing_architecture` (no PR, no label). If acceptance criteria missing: abort `blocked_missing_acceptance_criteria`. Stop here.
3. **Reuse-existing-PR check (Jira recovery / idempotent open):** Resolve whether a PR URL already exists for this ticket (orchestrator message `PR:`, prior handoff, Jira comments, or GitHub search by ticket key on the product repo).
   - If a real PR URL **already exists**: **skip opening a new PR**. Do **not** re-implement. Take the **jira-complete** path below (steps 5–7 only). This is the allowed label-complete path after `implementation_ready_jira_auth_required`.
   - If no PR exists yet: continue to step 4 (full open). Confirm `implement-change` produced a pushed ticket branch with code + tests (or equivalent ready-to-review commits).
4. Open **one** pull request against the product default branch (`FACTORY_PRODUCT_DEFAULT_BRANCH` / `main`):
   - Title references the ticket key.
   - Body includes summary, acceptance-criteria coverage, test notes, and links to approved architecture.
   - Do **not** merge. Do **not** request self-approval as final.
5. **Only after** the PR URL exists: add a Jira comment with the PR link (and short implementation summary).
6. Update factory stage labels **only** in this transition (and only after the PR URL exists and step 5 succeeded):
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
- If GitHub succeeds but Jira auth fails: leave stage at **`implementation`**, include the **PR URL**, and use status **`implementation_ready_jira_auth_required`**. Do **not** invent `pr_review`. Do **not** ask product (or anyone else) to set `pr_review` — you remain the sole writer; recovery is your jira-complete path after auth.
- Never open a second PR for the same ticket when a PR URL already exists.

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

When completing an existing PR (reuse path), say `Reused existing PR` instead of `Opened PR`.

## Reply when auth unavailable (after stage confirmed `implementation`)

```text
Implementation ready for <KEY> (PR and/or Jira not fully updated)
Handoff: orchestrator
Ticket: <KEY>
Stage: implementation
PR: <url or none>
Status: implementation_ready_github_auth_required|implementation_ready_jira_auth_required|implementation_ready_auth_required
```

When the PR already exists and only Jira failed, always set `Status: implementation_ready_jira_auth_required` and include `PR: <url>`.

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
