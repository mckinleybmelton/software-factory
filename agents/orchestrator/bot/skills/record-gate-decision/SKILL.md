---
description: Use when a human approves or rejects a factory review gate (PRD, design, architecture, or PR).
---

# Record a gate decision

## Inputs

- Ticket key
- Current review stage (`prd_review`, `design_review`, `architecture_review`, or `pr_review`)
- Decision: `approve` or `reject`
- Optional notes (required on reject)

## Transitions

| Current | Approve → | Reject → |
| --- | --- | --- |
| `prd_review` | `design_draft` | `prd_draft` |
| `design_review` | `architecture_draft` | `design_draft` |
| `architecture_review` | `implementation` | `architecture_draft` |
| `pr_review` | `done` | `implementation` |

## Procedure

1. Confirm the human explicitly approved or rejected. Do not infer approval from silence.
2. Tell the human the label change that should land on the ticket (remove old stage label, add new). In this slice, if Jira is unavailable to you, state the exact labels to apply and ask the human (or product peer) to apply them.
3. On **reject**, keep rejection notes with the ticket context for the next draft peer ask.
4. On **approve** of `prd_review` in this slice: advance mentally/labels to `design_draft`, then ask `design` once — expect "not implemented" — and report that later stages are stubbed.
5. Never approve your own specialist's work. Never skip a human gate.

## Reply shape

```text
Gate: <stage>
Decision: approve|reject
Next stage: <label>
Notes: <text or none>
Next action: <what you will do / what human must do>
```
