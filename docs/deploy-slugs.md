# Hosted deploy slugs and app-host wiring

The factory runtime remains six peer agents under `agents/`. Hosted bring-up
deploys each peer with a **lowercase slug** that matches
`defineConnection({ agent: "<slug>" })`.

Do **not** invent new agents — only deploy and wire the existing peers.

## Canonical slugs

| Directory | Deploy slug | Role |
| --- | --- | --- |
| `agents/orchestrator` | `orchestrator` | Entry peer; routes only |
| `agents/product` | `product` | PRDs, stage lookups / draft+`done` labels |
| `agents/design` | `design` | UX draft; sole `design_review` writer |
| `agents/architect` | `architect` | Architecture draft; sole `architecture_review` writer |
| `agents/implementer` | `implementer` | Code + PR; sole `pr_review` writer (after PR) |
| `agents/reviewer` | `reviewer` | PR review packet; **no** label writes |

## Deploy each peer

From a pushed git ref (hosting deploys remote source, not local dirty files):

```bash
npx --yes "@grok/agent-sdk@0.4.0" deploy --dir ./agents/orchestrator --slug orchestrator
npx --yes "@grok/agent-sdk@0.4.0" deploy --dir ./agents/product --slug product
npx --yes "@grok/agent-sdk@0.4.0" deploy --dir ./agents/design --slug design
npx --yes "@grok/agent-sdk@0.4.0" deploy --dir ./agents/architect --slug architect
npx --yes "@grok/agent-sdk@0.4.0" deploy --dir ./agents/implementer --slug implementer
npx --yes "@grok/agent-sdk@0.4.0" deploy --dir ./agents/reviewer --slug reviewer
```

Prefer dry-run before the first write if your workflow uses the Agent SDK
deploy skill / CLI dry-run flags.

After deploy, attach **Atlassian** (and **GitHub** for implementer/reviewer)
under each slug’s Deployed Agents connectors. Set product-repo env on the
**implementer** deployment. See [config-checklist.md](./config-checklist.md).

## Orchestrator → specialist connections

Local serve resolves peers by directory name under `--dir ./agents`. Hosted
connections must use the **same lowercase deploy slug**:

```ts
// agents/orchestrator/bot/mcp-connections/product.ts
import { defineConnection } from "@grok/agent-sdk/connections";

export default defineConnection({
  agent: "product",
  description: "Product peer: drafts PRDs and posts them to Jira.",
});
```

Same pattern for `design`, `architect`, `implementer`, `reviewer` in
`agents/orchestrator/bot/mcp-connections/`.

If you must use a non-default slug, keep connection `agent` values in sync with
the deploy `--slug` (and any env overrides). Prefer the canonical table above.

## App-host → orchestrator wiring

`examples/app-host` is a thin consumer. It does not replace the six peers; it
asks the orchestrator peer.

```ts
// examples/app-host/bot/mcp-connections/orchestrator.ts
import { defineConnection } from "@grok/agent-sdk/connections";

export default defineConnection({
  agent: process.env.FACTORY_ORCHESTRATOR_SLUG ?? "orchestrator",
  description:
    "Factory orchestrator: routes Jira tickets through specialist peers.",
});
```

| Mode | How the host finds `orchestrator` |
| --- | --- |
| Local | Serve factory peers (`serve --dir ./agents`) so slug `orchestrator` mounts |
| Hosted | Deploy orchestrator with `--slug orchestrator` (or set `FACTORY_ORCHESTRATOR_SLUG`) |
| Extensions | Mount `@software-factory/core` / plugin for skills; **routing** still goes through the orchestrator peer connection |

App-host also mounts packages via `bot/extensions/` (`factory.ts`,
`softwareFactory.ts`). Those mounts do not create specialist peers — specialists
stay the deployed (or locally served) slugs above.

### Install / validate host

```bash
cd examples/app-host
npm install
npx --yes "@grok/agent-sdk@0.4.0" validate --dir .
```

Unresolved orchestrator peer warnings are expected until peers are served or
deployed.

## Connection matrix (quick)

```text
Cursor / app-host
    └── ask → orchestrator
              ├── product
              ├── design
              ├── architect
              ├── implementer
              └── reviewer
```

Specialists return to the orchestrator only; they do not call each other.

## Related

- [config-checklist.md](./config-checklist.md)
- [smoke-e2e.md](./smoke-e2e.md)
- [examples/app-host/README.md](../examples/app-host/README.md)
