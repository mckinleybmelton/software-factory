# Architecture artifact contract

Required fields (all non-empty unless noted):

| Field | Meaning |
| --- | --- |
| `summary` | One short paragraph: how the system will be structured to deliver the approved PRD and design |
| `components` | Named building blocks with responsibility (services, modules, packages, or major units) |
| `boundaries` | Ownership, trust, data, and interface edges between components (what may / may not cross) |
| `dependency_graph` | Directed dependencies among components (mermaid flowchart preferred, or explicit adjacency list with edges) |
| `open_questions` | List (may be empty only when nothing is unknown; prefer residual tech risks and PRD/design gaps) |

## Source of truth

- Base the architecture **only** on the approved PRD and approved design (and explicit architecture-review rejection notes when re-drafting).
- Do not change product scope, acceptance criteria, or UX flows. Flag conflicts under `open_questions`.

Reject a draft that leaves `summary`, `components`, `boundaries`, or `dependency_graph` blank, or that has no concrete component entries or no directed edges.

Implementation, PR review packets, and product-scope changes are out of scope for the architect agent.
