# Design artifact contract

Required fields (all non-empty unless noted):

| Field | Meaning |
| --- | --- |
| `summary` | One short paragraph: what experience this ticket delivers for the approved PRD |
| `user_flows` | One or more named flows covering in-scope journeys (trigger, steps, success/failure) |
| `screens_interfaces` | Screens or interfaces needed: name, purpose, key elements (may include empty/error/loading notes) |
| `open_questions` | List (may be empty only when nothing is unknown; prefer listing residual UX risks and PRD gaps) |

## Source of truth

- Base the design **only** on the approved PRD (and explicit design-review rejection notes when re-drafting).
- Do not change product scope, acceptance criteria, or out-of-scope lists. Flag conflicts under `open_questions`.

Reject a draft that leaves `summary`, `user_flows`, or `screens_interfaces` blank, or that has no concrete screen/interface entries.

Architecture, dependency graphs, implementation, and PR review packets are out of scope for the design agent.
