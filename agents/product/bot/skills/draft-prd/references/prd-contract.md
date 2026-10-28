# PRD artifact contract

Required fields (all non-empty):

| Field | Meaning |
| --- | --- |
| `problem` | What pain or opportunity this ticket addresses |
| `users` | Who is affected / who benefits |
| `scope` | What this change will deliver |
| `out_of_scope` | Explicit non-goals for this ticket |
| `acceptance_criteria` | One or more testable pass/fail bullets |
| `open_questions` | List (may be empty only when nothing is unknown; prefer listing residual risks) |

Reject a draft that leaves `problem`, `users`, `scope`, `out_of_scope`, or `acceptance_criteria` blank.

Later artifacts (design, architecture with dependency graph, PR review packet) are out of scope for the product agent.
