# PR review packet contract

Required fields (all non-empty unless noted):

| Field | Meaning |
| --- | --- |
| `summary` | One short paragraph: how the PR relates to the approved PRD + architecture |
| `pr` | Canonical PR URL |
| `matches` | Acceptance criteria / architecture points the PR appears to satisfy |
| `gaps` | Missing or mismatched criteria, architecture boundary issues, test holes (may be empty only when nothing is missing) |
| `ci_tests` | What was observed about CI/tests (or explicit “unavailable”) |
| `recommendation` | Non-binding hint for the human: `approve` or `changes_requested` — never an automated merge |

## Source of truth

- Base the review on the **PR diff**, available **CI/tests**, the **approved PRD** (acceptance criteria), and the **approved architecture**.
- Do not change product scope, UX, or architecture. Do not write product code.

Reject a packet that lacks a PR URL, omits matches/gaps sections, or claims the human already approved/merged.
