---
description: Use when implementing approved architecture for a factory ticket already at implementation, before opening a PR.
---

# Implement change

Follow the product-repo and isolation rules in `references/product-repo.md`.

## Procedure

1. Confirm stage is already **`implementation`** (orchestrator message and/or Jira). If not, stop and hand back `blocked_wrong_stage` — do not create branches or commits.
2. Read the **approved architecture** (components, boundaries, dependency graph) and **acceptance criteria** from the approved PRD. Include any prior `pr_review` rejection notes when re-implementing.
3. Resolve the **product repo** from config (`FACTORY_PRODUCT_REPO` / `PRODUCT_REPO`, optional local path). If unresolved, abort with `blocked_missing_product_repo`.
4. Create or reuse **one** branch for this ticket (name should include the ticket key). Prefer a **git worktree** (or equivalent isolated checkout) so concurrent tickets never share a dirty working tree. Never commit on the product default branch.
5. Implement the change to satisfy acceptance criteria and the dependency graph order. Add or update tests that cover the acceptance criteria.
6. Run the product repo’s usual test/lint commands when available; fix failures you introduced.
7. Commit on the ticket branch with a clear message referencing the ticket key. Do **not** open the PR yet — that is `open-pr`.
8. Summarize what changed, how tests were verified, and any residual gaps for the PR body.

## Output shape (before open-pr)

```markdown
## Implementation

### Summary
...

### Branch
`<branch-name>` in `<owner/repo>`

### Changes
- ...

### Tests
- ...

### Open questions
- ...
```

## Hard rules

- Do not merge. Do not set `pr_review`. Do not approve.
- Do not rewrite PRD, design, or architecture. Flag conflicts under open questions.
- One ticket → one branch. Keep the diff scoped.
