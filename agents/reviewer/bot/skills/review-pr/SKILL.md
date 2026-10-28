---
description: Use when reviewing a product-repo PR for a factory ticket already at pr_review, before posting the review packet to Jira.
---

# Review PR

Follow the packet contract in `references/review-packet-contract.md`.

## Procedure

1. Confirm stage is already **`pr_review`**. If not, stop with `blocked_wrong_stage` — no packet post, no label changes.
2. Resolve the PR URL from the orchestrator message, Jira comments, or GitHub (ticket key / branch). If missing: abort `blocked_missing_pr`.
3. Read the PR diff (GitHub MCP or `gh`). Note CI/check conclusions when available; if CI is unavailable, say so under gaps/assumptions — do not invent green checks.
4. Read the **approved PRD acceptance criteria** and **approved architecture**. If either is missing: abort with `blocked_missing_acceptance_criteria` or `blocked_missing_architecture`.
5. Compare the diff (+ tests/CI) to acceptance criteria and architecture boundaries/dependency expectations.
6. Produce the review packet: matches, gaps, PR link. Do not write product code. Do not approve. Do not merge.

## Output shape (before Jira post)

```markdown
## PR review

### Summary
...

### PR
<url>

### Matches
- ...

### Gaps
- ...

### CI / tests
- ...

### Recommendation for human
approve | changes_requested (human decides; you do not merge)
```
