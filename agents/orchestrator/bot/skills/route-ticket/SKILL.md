---
description: Use when routing a Jira ticket through factory stages — pick stage, peer, and next action.
---

# Route a ticket

## Inputs

- Ticket key (e.g. `ASF-12`)
- Current factory stage label on the ticket (if unknown, ask the human or have **`product`** read Jira — **never** ask `design` for stage lookup or label updates)
- Human intent: start, continue, approve, reject, status

## Stage → peer

| Stage label | Peer to ask | Action |
| --- | --- | --- |
| `prd_draft` | `product` | Ask product to draft PRD and post to Jira |
| `prd_review` | _(none)_ | **Human gate** — stop; wait for approve/reject |
| `design_draft` | `design` | Ask design to draft UX and post to Jira (**only** after stage is confirmed `design_draft`) |
| `design_review` | _(none)_ | **Human gate** — stop; wait for approve/reject |
| `architecture_draft` | `architect` | Ask architect peer (stub) |
| `architecture_review` | _(none)_ | Human gate |
| `implementation` | `implementer` | Ask implementer peer (stub) |
| `pr_review` | `reviewer` | Ask reviewer peer (stub) |
| `done` | _(none)_ | Report complete; no further routing |

## Jira ownership

| Need | Who |
| --- | --- |
| Stage lookup / label apply (including post-gate `design_draft`, `architecture_draft`, return-to-draft) | **`product`** or human |
| UX draft + post → `design_review` | **`design`** only, and only when stage is already `design_draft` |

Do **not** send generic Jira reads or label updates to `design`. Design is not a catch-all Jira peer.

## Procedure

1. Resolve the ticket key and current stage label (human or **product** Jira read).
2. If stage is a `*_review` gate, do **not** ask a specialist to approve. Summarize and wait for the human.
3. If stage is a draft/implementation stage, ask the matching peer with scoped context: ticket key, stage, relevant notes, rejection feedback if any.
4. Before asking `design`, confirm the ticket stage is already `design_draft`. If a gate decision just advanced labels, wait until product (or human) confirms the label landed — do not race a deferred `design_draft` write against design's `design_review` post.
5. After the peer returns, report status:
   - Product success (PRD post) → expect `prd_review` and **stop** for human review.
   - Design success → expect `design_review` and **stop** for human review.
   - Design **abort** / `blocked_*` → do **not** treat as `design_review`. Handle **only** by the specific status below (do not collapse them into one path):
     - `blocked_wrong_stage`: have **product** read the actual stage **now**. Route **only** from that live stage (human `*_review` → stop; draft/implementation → matching peer). Do **not** apply `design_draft` because an earlier turn once approved PRD/design — a stale authorize must not rewind `architecture_*` / later stages. Resume a pending label apply **only** inside the same in-progress `record-gate-decision` flow when the live stage is still that gate's "from" label (e.g. still `prd_review` after this approve, or still `design_review` after this reject); then verify before asking design.
     - `blocked_wrong_ask`: ask **product** (or human) for the Jira read/label work; **no** stage change; **do not** re-ask design.
     - `blocked_missing_prd`: **no** label rewrite. If live stage is `design_draft`, supply the approved PRD (or have product fetch it), verify stage is still `design_draft`, then re-ask design. If live stage is anything else, route from that stage instead of re-asking design.
   - Design `design_ready_jira_auth_required` → stage remains `design_draft`; do not open the human design gate until a real post sets `design_review`.
6. On reject (via `record-gate-decision`), product/human returns stage to the draft label; **verify** that draft label, then re-ask that peer with the rejection notes. Never race a deferred draft-label write against a specialist post.

## Peer ask shapes

When asking `product` to **apply a stage label** (after a gate decision), include at least:

```text
Ticket: <KEY>
Task: Apply factory stage labels only — remove <old_stage> (and any other factory stage labels), add <new_stage>. Confirm the resulting stage label. Do not draft a PRD or design.
```

When asking `product` to **read stage**, include at least:

```text
Ticket: <KEY>
Task: Read the ticket and report the current factory stage label only.
```

When asking `product` for a PRD draft, include at least:

```text
Ticket: <KEY>
Stage: prd_draft
Task: Draft the PRD (problem, users, scope, out of scope, acceptance criteria, open questions), post it to Jira, set label to prd_review, and hand back. Do not approve.
```

When asking `design`, include at least:

```text
Ticket: <KEY>
Stage: design_draft
Task: Stage is already design_draft. Read the approved PRD only. Draft design (user flows, screens/interfaces), post it to Jira, set label to design_review, and hand back. Do not approve. Do not apply design_draft.
```

Include the approved PRD body (or a pointer to the Jira PRD comment) and any prior `design_review` rejection notes.
