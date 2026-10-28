---
description: Use when drafting architecture for a factory ticket already at architecture_draft, before posting to Jira.
---

# Draft architecture

Follow the field contract in `references/architecture-contract.md`.

## Procedure

1. Confirm the ticket stage is already **`architecture_draft`** (orchestrator message and/or Jira). If not, do **not** draft; hand back `blocked_wrong_stage` with the actual stage. Do not tell anyone to force-apply `architecture_draft`.
2. Read the approved PRD and approved design from the ticket (summary, description, PRD comment, design comment). Include any rejection notes from a prior `architecture_review`. If PRD missing: `blocked_missing_prd`. If design missing: `blocked_missing_design`.
3. Derive **components** that cover the design screens/flows and PRD acceptance criteria. Do not invent product goals outside the PRD.
4. Define **boundaries** (ownership, trust, data, and interface edges between components).
5. Build a **dependency graph**: directed edges showing what depends on what (build/runtime). Prefer a mermaid `flowchart` or adjacency list that implementers can follow.
6. Put unknowns and PRD/design gaps in **open questions** instead of guessing product or UX intent.
7. Validate mentally against the contract before posting.

## Output shape (before Jira post)

```markdown
## Architecture

### Summary
...

### Components
| Component | Responsibility | Notes |
| --- | --- | --- |
| ... | ... | ... |

### Boundaries
- ...

### Dependency graph
```mermaid
flowchart TD
  A --> B
```

### Open questions
- ...
```
