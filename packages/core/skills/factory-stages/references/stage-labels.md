# Factory stage labels

Ordered pipeline (exactly one on the ticket):

| Label | Meaning |
| --- | --- |
| `prd_draft` | Product drafts the PRD |
| `prd_review` | Human PRD gate |
| `design_draft` | Design drafts UX |
| `design_review` | Human design gate |
| `architecture_draft` | Architect drafts architecture |
| `architecture_review` | Human architecture gate |
| `implementation` | Implementer codes + opens PR |
| `pr_review` | Reviewer packet + human PR gate (set only after a PR exists) |
| `done` | Finished |

## Transitions

- **Submit:** `*_draft` → matching `*_review` (or implementer → `pr_review` after PR exists).
- **Approve:** review → next draft / `implementation` / `done`.
- **Reject / changes_requested:** review → same draft (PR reject → `implementation`) with notes.

Who writes review labels: design → `design_review`, architect → `architecture_review`, implementer → `pr_review`. Product owns generic stage lookups and other label applies for the orchestrator. Reviewer never writes stage labels.
