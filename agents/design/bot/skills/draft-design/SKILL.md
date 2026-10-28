---
description: Use when drafting UX design artifacts for a factory ticket after PRD approval, before posting to Jira.
---

# Draft design

Follow the field contract in `references/design-contract.md`.

## Procedure

1. Read the approved PRD from the ticket (summary, description, and the PRD comment). Include any rejection notes from a prior `design_review`.
2. Derive **user flows** that cover the acceptance criteria and in-scope journeys. Do not invent product goals outside the PRD.
3. List **screens / interfaces** needed for those flows (purpose, key elements, empty/error/loading where relevant).
4. Put unknowns and PRD gaps in **open questions** instead of guessing product intent.
5. Validate mentally against the contract before posting.

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
