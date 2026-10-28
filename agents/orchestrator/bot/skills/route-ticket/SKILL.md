---
description: Use when routing a Jira ticket through factory stages — pick stage, peer, and next action.
---

# Route a ticket

## Inputs

- Ticket key (e.g. `ASF-12`)
- Current factory stage label on the ticket (if unknown, ask the human or have product/design read Jira)
- Human intent: start, continue, approve, reject, status

## Stage → peer

| Stage label | Peer to ask | Action |
| --- | --- | --- |
| `prd_draft` | `product` | Ask product to draft PRD and post to Jira |
| `prd_review` | _(none)_ | **Human gate** — stop; wait for approve/reject |
| `design_draft` | `design` | Ask design to draft UX and post to Jira |
| `design_review` | _(none)_ | **Human gate** — stop; wait for approve/reject |
| `architecture_draft` | `architect` | Ask architect peer (stub) |
| `architecture_review` | _(none)_ | Human gate |
| `implementation` | `implementer` | Ask implementer peer (stub) |
| `pr_review` | `reviewer` | Ask reviewer peer (stub) |
| `done` | _(none)_ | Report complete; no further routing |

## Procedure

1. Resolve the ticket key and current stage label.
2. If stage is a `*_review` gate, do **not** ask a specialist to approve. Summarize and wait for the human.
3. If stage is a draft/implementation stage, ask the matching peer with scoped context: ticket key, stage, relevant notes, rejection feedback if any.
4. After the peer returns, report status:
   - Product success → expect `prd_review` and **stop** for human review.
   - Design success → expect `design_review` and **stop** for human review.
5. On reject (via `record-gate-decision`), stage returns to the same draft; re-ask that peer with the rejection notes.

## Peer ask shapes

When asking `product`, include at least:

```text
Ticket: <KEY>
Stage: prd_draft
Task: Draft the PRD (problem, users, scope, out of scope, acceptance criteria, open questions), post it to Jira, set label to prd_review, and hand back. Do not approve.
```

When asking `design`, include at least:

```text
Ticket: <KEY>
Stage: design_draft
Task: Read the approved PRD only. Draft design (user flows, screens/interfaces), post it to Jira, set label to design_review, and hand back. Do not approve.
```

Include the approved PRD body (or a pointer to the Jira PRD comment) and any prior `design_review` rejection notes.
