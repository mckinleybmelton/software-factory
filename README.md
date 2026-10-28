# software-factory

Creating an AI software factory for building personal projects the way industry leaders are.

This repository is the factory. Jira is the source of truth for the ticket and the current stage. This first slice is a Python 3 command-line tool: a deterministic orchestrator, a stage machine, a Jira adapter, and a product agent. Design, architect, implementer, and reviewer are named in the stage model and do not run. There is no web service. The commands do not open a branch or change a product repository.

A person still approves the PRD before any later stage can start. The product agent drafts the PRD from the ticket. The orchestrator does not write that text itself.

## Setup

Python 3.11 or newer. From a checkout:

```bash
pip install -e ".[dev]"
```

## Configure

Credentials and the project key come from the environment. Do not commit them.

| Variable | Purpose |
| --- | --- |
| `JIRA_BASE_URL` | Site URL, for example `https://your-site.atlassian.net` |
| `JIRA_EMAIL` | Email of the Jira user that owns the API token |
| `JIRA_API_TOKEN` | API token. The adapter sends HTTP basic auth as `email:token` |
| `JIRA_PROJECT_KEY` | Project key, for example `SF` |

```bash
export JIRA_BASE_URL="https://your-site.atlassian.net"
export JIRA_EMAIL="you@example.com"
export JIRA_API_TOKEN="your-token"
export JIRA_PROJECT_KEY="SF"
```

The current stage is a label on the ticket. The label text defaults to the stage name: `prd_draft`, `prd_review`, `design_draft`, `design_review`, `architecture_draft`, `architecture_review`, `implementation`, `pr_review`, `done`. A ticket with no stage label is treated as `prd_draft`.

Override any label with `FACTORY_STAGE_LABELS`, a JSON object of stage name to label text:

```bash
export FACTORY_STAGE_LABELS='{"prd_review":"sf-prd-review"}'
```

The adapter uses Jira REST API v2. It reads the ticket, posts a comment, and replaces the stage label without removing other labels.

## Commands

Draft a PRD from the ticket summary and description, post it as a Jira comment, and set the stage to `prd_review`. The process exits 0. If the stage is anything other than `prd_draft` (or missing), the process exits with an error: this build only runs the product agent.

```bash
python -m factory run SF-1
```

Record the human decision on the PRD gate. The command comments on the ticket and updates the stage label. It does not generate a design.

```bash
python -m factory resume SF-1 approved --note "Ready for design."
python -m factory resume SF-1 changes_requested --note "Name the users and the acceptance criteria."
```

`approved` is accepted only from `prd_review` and moves the label to `design_draft`. `changes_requested` returns the label to `prd_draft` and keeps the note on the ticket.

Fields the ticket already states are copied into the PRD and marked as coming from the ticket. Users, scope, out of scope, and acceptance criteria that the ticket does not state are explicit unanswered placeholders, and each gap is also an open question.

## Tests

```bash
python -m pytest
```

Tests use an in-memory Jira adapter and do not call the network.
