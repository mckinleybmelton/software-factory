# Factory conventions

Exactly one factory stage label on a Jira ticket:

`prd_draft` → `prd_review` → `design_draft` → `design_review` → `architecture_draft` → `architecture_review` → `implementation` → `pr_review` → `done`

- Submit: draft → matching review (implementer sets `pr_review` only after a PR exists).
- Approve: review → next draft / `implementation` / `done`.
- Reject / changes_requested: review → same draft (or `implementation` for PR reject) with notes.

Specialists return to the **orchestrator**; they do not call each other.

When finishing ticket-scoped work, end with a handoff block. Load skill `factory-stages` for the label list and handoff template details.
