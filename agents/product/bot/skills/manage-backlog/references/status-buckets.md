# Backlog config — status buckets and scope

## Scope (env or ask)

| Source | Meaning |
| --- | --- |
| `JIRA_PROJECT_KEY` or `FACTORY_JIRA_PROJECT` | Default Jira project key (e.g. `ASF`) |
| `JIRA_FILTER_ID` | Optional saved filter id when triage is filter-scoped |
| `JIRA_BOARD_ID` | Optional board id when triage is board-scoped |
| User message | Named project, filter, or board overrides env for that turn |

If none are set, ask once for the project key (or filter/board name).

## Status → bucket map

Match **case-insensitively** on the issue's current status name. First matching bucket wins. Env override (optional JSON object of bucket → comma-separated status names):

`FACTORY_BACKLOG_STATUS_MAP` example:

```json
{
  "yet_to_start": "To Do,Open,Backlog,Selected for Development,New,Ready",
  "in_progress": "In Progress,In Development,Doing,Building",
  "in_review": "In Review,Review,Code Review,PR Review,QA,In QA,Pending Review",
  "finished": "Done,Closed,Resolved,Complete,Cancelled,Canceled"
}
```

### Defaults (common Jira / company-managed + team-managed names)

| Bucket | Status names |
| --- | --- |
| `yet_to_start` | To Do, Open, Backlog, Selected for Development, New, Ready, Todo |
| `in_progress` | In Progress, In Development, Doing, Building, Implementing |
| `in_review` | In Review, Review, Code Review, PR Review, QA, In QA, Pending Review, Awaiting Approval |
| `finished` | Done, Closed, Resolved, Complete, Completed, Cancelled, Canceled |

Unknown status → treat as `in_progress` and note under assumptions.

## Factory stage labels

Exactly one (when present) among:

`prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`

- `*_review` (`prd_review`, `design_review`, `architecture_review`, `pr_review`) → human gate only (propose wait; do not approve). Exclude from **Start** next-steps even when status is `yet_to_start` and unblocked.
- Draft / `implementation` needing work → eligible for **Start** (when unblocked) or hand off to orchestrator for a stage run.
- Label `done` usually aligns with bucket `finished`.

## Stale threshold

| Source | Meaning |
| --- | --- |
| `FACTORY_BACKLOG_STALE_DAYS` | Days since last update to call an open issue stale (default **7**) |

## Explicit move rules (examples — only when user states them)

- Mark `in_review` items stale after N days (comment and/or label; do not invent priority).
- After human gate approval: advance factory stage label per factory rules; do not approve yourself.
- On `changes_requested` / reject: return factory stage to the matching `*_draft` (or prior draft) with notes.

Never reshuffle rank/priority without a stated rule.
