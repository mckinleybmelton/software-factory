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

## Who writes labels / who reads stage

- You have **no** Jira. Stage label applies and stage lookups go to **`product`** (or the human). **Never** ask `design` to read stage or apply labels.
- `design` only runs when stage is already confirmed `design_draft`, and is the **only** peer that writes `design_review` (via its post skill after drafting UX).

## Procedure

1. Confirm the human explicitly approved or rejected. Do not infer approval from silence.
2. Tell the human the label change that should land on the ticket (remove old stage label, add new). Ask **`product`** (or the human) to apply that exact label change. Do **not** ask `design` to apply labels.
3. On **reject** / **changes_requested**, keep rejection notes with the ticket context for the next draft peer ask.
4. On **approve** of `prd_review`:
   1. Ask **`product`** to apply labels only: remove `prd_review` (and any other factory stage labels), add **`design_draft`**. Do **not** ask design yet.
   2. **Verify** stage is `design_draft` (ask product to read the ticket labels, or confirm with the human). Do not proceed on assumption.
   3. Only after verification, ask `design` to draft UX from the approved PRD and post to Jira (`design_review`). When design returns at `design_review`, **stop** for the human gate.
5. On **approve** of `design_review`:
   1. Ask **`product`** (or human) to apply `architecture_draft`.
   2. Verify stage is `architecture_draft`, then ask `architect` once — expect "not implemented" — and report that later stages are stubbed.
6. On **reject** of `design_review`:
   1. Ask **`product`** (or human) to apply **`design_draft`** only (return from `design_review`).
   2. **Verify** stage is `design_draft` before re-asking `design` with the notes.
7. Never approve your own specialist's work. Never skip a human gate.
8. Never ask `design` in the same turn as a deferred `design_draft` label write — wait until the draft label is confirmed on the ticket.

## Reply shape

```text
Gate: <stage>
Decision: approve|reject
Next stage: <label>
Notes: <text or none>
Label apply: product|human (pending|confirmed)
Next action: <what you will do / what human must do>
```
