# Product-repo and auth config checklist

Copy-paste checklist for bring-up. No new agents — configure the existing six
peers and (optionally) an app-host.

## 0. One-command setup (recommended)

From a factory checkout, this covers runtime install, validate, `.env.factory`
product-repo config, optional login, and optional serve:

```bash
./scripts/setup-factory.sh --product-repo owner/name --login --serve
# optional: --product-path ../your-app --jira-project KEY
# later:    ./scripts/serve-factory.sh
```

Still required once (dashboard): Atlassian + GitHub MCP connectors (step 3).
After serve: create a `prd_draft` ticket and talk to the orchestrator
([smoke-e2e.md](./smoke-e2e.md)).

## 1. Runtime

```bash
# Node 22.13+ (never Bun)
node -v

cd /path/to/software-factory
npm install
# or: for d in agents/*/; do (cd "$d" && npm install); done

npx --yes "@grok/agent-sdk@0.4.0" validate --dir ./agents
```

Or use `./scripts/setup-factory.sh` (section 0) instead of steps 1–2 / 4 / 7.

## 2. Cursor credential (model turns + account MCP)

```bash
npx --yes "@grok/agent-sdk@0.4.0" login
# or:
export CURSOR_API_KEY=...
```

Unsigned local playground only (trusted networks):

```bash
npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev \
  --allow-anonymous --allow-anonymous-cursor-account-mcp
```

`validate` stays green without a credential. `serve` / `eval` / chat need one
for real model turns.

## 3. MCP connectors

| Peer | Connectors | Where |
| --- | --- | --- |
| `product`, `design`, `architect` | Atlassian | Cursor dashboard → MCP, or Deployed Agents connectors |
| `implementer` | Atlassian + GitHub | same |
| `reviewer` | Atlassian + GitHub (read) | same |
| `orchestrator` | Peer agents only (no Jira) | local serve mounts / hosted deploy slugs |

Wiring in-repo: `agents/*/bot/mcp-connections/` use
`defineConnection({ cursorAccount: true, servers: ["Atlassian"|…], optional: true })`
so missing OAuth does not fail **validate**.

Checklist:

- [ ] Atlassian connected and authorized for product / design / architect / implementer / reviewer
- [ ] GitHub connected for implementer (and reviewer)
- [ ] Hosted: same servers attached under each deploy slug’s connectors
- [ ] Smoke: product can read a ticket; implementer can see the product repo

## 4. Product repo (implementer)

| Variable | Required | Example | Meaning |
| --- | --- | --- | --- |
| `FACTORY_PRODUCT_REPO` or `PRODUCT_REPO` | Yes (live implement) | `acme/widget-app` | GitHub `owner/name` |
| `FACTORY_PRODUCT_REPO_PATH` or `PRODUCT_REPO_PATH` | No | `/work/widget-app` | Local checkout / cache |
| `FACTORY_PRODUCT_DEFAULT_BRANCH` or `PRODUCT_DEFAULT_BRANCH` | No | `main` | PR base (default `main`) |

```bash
export FACTORY_PRODUCT_REPO=owner/name
# optional:
export FACTORY_PRODUCT_REPO_PATH=/path/to/checkout
export FACTORY_PRODUCT_DEFAULT_BRANCH=main
```

Rules:

- Factory repo is **not** the product repo unless config points there.
- Missing repo → `blocked_missing_product_repo` (no git side effects).
- Missing architecture or acceptance criteria → `blocked_missing_*` **before**
  any worktree, branch, or commit.

Detail: `agents/implementer/bot/skills/implement-change/references/product-repo.md`.

## 5. Jira / backlog defaults (product)

| Variable | Role |
| --- | --- |
| `JIRA_PROJECT_KEY` / `FACTORY_JIRA_PROJECT` | Default project key |
| `JIRA_FILTER_ID` / `JIRA_BOARD_ID` | Optional backlog scope |
| `FACTORY_BACKLOG_STATUS_MAP` | Optional status → bucket overrides |
| `FACTORY_BACKLOG_STALE_DAYS` | Optional stale threshold |

Stage truth is always the **single** factory stage label on the ticket.

## 6. App-host / peer override

| Variable | Role |
| --- | --- |
| `FACTORY_ORCHESTRATOR_SLUG` | Host → orchestrator peer slug (default `orchestrator`) |

See [deploy-slugs.md](./deploy-slugs.md) for hosted peer slugs and
`examples/app-host` connection wiring.

## 7. Quick verify

```bash
npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev
# Open http://127.0.0.1:3000/orchestrator/playground
# "Read stage for ticket <KEY>" → product peer + Atlassian
```

Then follow [smoke-e2e.md](./smoke-e2e.md).
