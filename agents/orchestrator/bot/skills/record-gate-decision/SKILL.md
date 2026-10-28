---
description: Use when a human approves or rejects a factory review gate (PRD, design, architecture, or PR).
---

# Record a gate decision

## Inputs

- Ticket key
- Current review stage (`prd_review`, `design_review`, `architecture_review`, or `pr_review`)
- Decision: `approve` or `reject` (also accept `changes_requested` as reject)
- Optional notes (required on reject / changes_requested)

## Transitions

| Current | Approve → | Reject / changes_requested → |
| --- | --- | --- |
| `prd_review` | `design_draft` | `prd_draft` |
| `design_review` | `architecture_draft` | `design_draft` |
| `architecture_review` | `implementation` | `architecture_draft` |
| `pr_review` | `done` | `implementation` |

## Procedure

1. Confirm the human explicitly approved or rejected. Do not infer approval from silence.
2. Tell the human the label change that should land on the ticket (remove old stage label, add new). If Jira is unavailable to you, state the exact labels to apply and ask the human (or product/design peer) to apply them.
3. On **reject** / **changes_requested**, keep rejection notes with the ticket context for the next draft peer ask.
4. On **approve** of `prd_review`: advance labels to `design_draft`, then ask `design` to draft UX from the approved PRD and post to Jira. When design returns at `design_review`, **stop** for the human gate.
5. On **approve** of `design_review`: advance labels to `architecture_draft`, then ask `architect` once — expect "not implemented" — and report that later stages are stubbed.
6. On **reject** of `design_review`: return to `design_draft` and re-ask `design` with the notes.
7. Never approve your own specialist's work. Never skip a human gate.

## Reply shape

```text
Gate: <stage>
Decision: approve|reject
Next stage: <label>
Notes: <text or none>
Next action: <what you will do / what human must do>
```
