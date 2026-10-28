---
description: Use when drafting UX for a factory ticket already at design_draft, before posting to Jira.
---

# Draft design

Follow the field contract in `references/design-contract.md`.

## Procedure

1. Confirm the ticket stage is already **`design_draft`** (orchestrator message and/or Jira). If not, do **not** draft; hand back `blocked_wrong_stage` with the actual stage. Do not tell anyone to force-apply `design_draft`.
2. Read the approved PRD from the ticket (summary, description, and the PRD comment). Include any rejection notes from a prior `design_review`. If the PRD is missing, hand back `blocked_missing_prd`.
3. Derive **user flows** that cover the acceptance criteria and in-scope journeys. Do not invent product goals outside the PRD.
4. List **screens / interfaces** needed for those flows (purpose, key elements, empty/error/loading where relevant).
5. Put unknowns and PRD gaps in **open questions** instead of guessing product intent.
6. Validate mentally against the contract before posting.

## Output shape (before Jira post)

```markdown
## Design

### Summary
...

### User flows
1. **Flow name** — trigger → steps → success / failure

### Screens / interfaces
| Screen | Purpose | Key elements |
| --- | --- | --- |
| ... | ... | ... |

### Open questions
- ...
```
