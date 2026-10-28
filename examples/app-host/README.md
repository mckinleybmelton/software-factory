# App host example

Thin Agent SDK host that mounts factory packages and documents how an app repo
installs the software factory.

## Install paths

### 1. GitHub clone (full peer network)

```bash
git clone https://github.com/mckinleybmelton/software-factory.git
cd software-factory
for d in agents/*/; do (cd "$d" && npm install); done
npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev
# Talk to http://127.0.0.1:3000/orchestrator/playground
```

Six peers stay the runtime: orchestrator, product, design, architect, implementer, reviewer.

### 2. Extension mount (this example)

From the monorepo root (or after publishing packages):

```bash
cd examples/app-host
npm install
npx --yes "@grok/agent-sdk@0.4.0" validate --dir .
```

Mount files:

| File | Mounts |
| --- | --- |
| `bot/extensions/factory.ts` | `@software-factory/core` |
| `bot/extensions/softwareFactory.ts` | `cursorPlugin({ path: "../../plugins/software-factory" })` |
| `bot/mcp-connections/orchestrator.ts` | peer `agent: orchestrator` (or `FACTORY_ORCHESTRATOR_SLUG`) |

In your own app agent, install packages and add one mount each:

```ts
// bot/extensions/factory.ts
import factory from "@software-factory/core";
export default factory();
```

```ts
// bot/extensions/productSkills.ts  (on a product-shaped agent)
import productSkills from "@software-factory/product-skills";
export default productSkills();
```

Copy or submodule `plugins/software-factory`, then:

```ts
import { cursorPlugin } from "@grok/agent-sdk/extensions";
export default cursorPlugin({ path: "plugins/software-factory" });
```

### 3. Deploy slugs (hosted peers)

Deploy each peer from this repo (slug usually matches the directory name):

```bash
agent-sdk deploy --dir ./agents/orchestrator --slug orchestrator
agent-sdk deploy --dir ./agents/product --slug product
agent-sdk deploy --dir ./agents/design --slug design
agent-sdk deploy --dir ./agents/architect --slug architect
agent-sdk deploy --dir ./agents/implementer --slug implementer
agent-sdk deploy --dir ./agents/reviewer --slug reviewer
```

On the host agent, peer connections use the **lowercase deploy slug**:

```ts
defineConnection({ agent: "orchestrator", description: "Factory orchestrator" });
```

Override with `FACTORY_ORCHESTRATOR_SLUG` when the slug differs. Orchestrator peers to specialists the same way (`product`, `design`, …).

## Env

| Variable | Role |
| --- | --- |
| `PRODUCT_REPO` / `FACTORY_PRODUCT_REPO` | Product git repo (`owner/name`) for implementer |
| `FACTORY_PRODUCT_REPO_PATH` | Optional local path override |
| `FACTORY_PRODUCT_DEFAULT_BRANCH` | Default `main` |
| `JIRA_PROJECT_KEY` / `FACTORY_JIRA_PROJECT` | Default Jira project |
| `JIRA_FILTER_ID` / `JIRA_BOARD_ID` | Optional backlog scope |
| `FACTORY_ORCHESTRATOR_SLUG` | Peer slug for this host (default `orchestrator`) |

Connect **Atlassian** (and **GitHub** for implementer/reviewer) in the Cursor dashboard. Sign the serve host in (`agent-sdk login` or `CURSOR_API_KEY`).

## Validate

```bash
npx --yes "@grok/agent-sdk@0.4.0" validate --dir .
```

Single-agent validate may warn that the orchestrator peer is unresolved until you serve with the factory peers or deploy them — that is expected.
