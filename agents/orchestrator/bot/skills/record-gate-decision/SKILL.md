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

- You have **no** Jira. Stage label applies and stage lookups go to **`product`** (or the human). **Never** ask `design`, `architect`, `implementer`, or `reviewer` to apply generic labels or look up stage (except implementer's sole `pr_review` write after a PR exists, and reviewer's review-packet comment with no label write).
- `design` only runs when stage is already confirmed `design_draft`, and is the **only** peer that writes `design_review` (via its post skill after drafting UX).
- `architect` only runs when stage is already confirmed `architecture_draft`, and is the **only** peer that writes `architecture_review` (via its post skill after drafting architecture).
- `implementer` only runs when stage is already confirmed `implementation`, and is the **only** peer that writes `pr_review` (via `open-pr` **after** the PR exists).
- `reviewer` only runs when stage is already confirmed `pr_review`, posts the review packet, and **never** writes `done` or `implementation`.

## Procedure

1. Confirm the human explicitly approved or rejected. Do not infer approval from silence.
2. Tell the human the label change that should land on the ticket (remove old stage label, add new). Ask **`product`** (or the human) to apply that exact label change. Do **not** ask design/architect/implementer/reviewer to apply gate-transition labels.
3. On **reject** / **changes_requested**, keep rejection notes with the ticket context for the next draft/implement peer ask.
4. On **approve** of `prd_review`:
   1. Ask **`product`** to apply labels only: remove `prd_review` (and any other factory stage labels), add **`design_draft`**. Do **not** ask design yet.
   2. **Verify** stage is `design_draft` (ask product to read the ticket labels, or confirm with the human). Do not proceed on assumption.
   3. Only after verification, ask `design` to draft UX from the approved PRD and post to Jira (`design_review`). When design returns at `design_review`, **stop** for the human gate.
5. On **approve** of `design_review`:
   1. Ask **`product`** to apply labels only: remove `design_review` (and any other factory stage labels), add **`architecture_draft`**. Do **not** ask architect yet.
   2. **Verify** stage is `architecture_draft`.
   3. Only after verification, ask `architect` to draft architecture (components, boundaries, dependency graph) from the approved PRD and design and post to Jira (`architecture_review`). When architect returns at `architecture_review`, **stop** for the human gate.
6. On **reject** of `design_review`:
   1. Ask **`product`** (or human) to apply **`design_draft`** only (return from `design_review`).
   2. **Verify** stage is `design_draft` before re-asking `design` with the notes.
7. On **approve** of `architecture_review`:
   1. Ask **`product`** (or human) to apply labels only: remove `architecture_review` (and any other factory stage labels), add **`implementation`**. Do **not** ask implementer yet.
   2. **Verify** stage is `implementation`.
   3. Only after verification, ask `implementer` to implement, open one PR, comment the PR link, and set `pr_review` only after the PR exists. When implementer returns at `pr_review`, **verify** `pr_review`, ask `reviewer` for the packet, then **stop** for the human PR gate.
8. On **reject** of `architecture_review`:
   1. Ask **`product`** (or human) to apply **`architecture_draft`** only (return from `architecture_review`).
   2. **Verify** stage is `architecture_draft` before re-asking `architect` with the notes.
9. On **approve** of `pr_review`:
   1. Ask **`product`** (or human) to apply **`done`**.
   2. **Verify** stage is `done`. Do **not** ask reviewer or implementer to merge. Report complete.
10. On **reject** of `pr_review`:
   1. Ask **`product`** (or human) to apply **`implementation`** only (return from `pr_review`).
   2. **Verify** stage is `implementation` before re-asking `implementer` with the notes.
11. Never approve your own specialist's work. Never skip a human gate. Never merge.
12. Never ask `design` in the same turn as a deferred `design_draft` label write — wait until the draft label is confirmed on the ticket.
13. Never ask `architect` in the same turn as a deferred `architecture_draft` label write — wait until the draft label is confirmed on the ticket.
14. Never ask `implementer` in the same turn as a deferred `implementation` label write — wait until `implementation` is confirmed on the ticket.
15. Never ask `reviewer` until stage is confirmed `pr_review`.

## Reply shape

```text
Gate: <stage>
Decision: approve|reject
Next stage: <label>
Notes: <text or none>
Label apply: product|human (pending|confirmed)
Next action: <what you will do / what human must do>
```
