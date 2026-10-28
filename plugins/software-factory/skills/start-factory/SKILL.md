---
name: start-factory
description: Use when starting or explaining a software-factory ticket run (PRD through PR review).
---

# Start the software factory

This plugin is an adapter. The full factory is six Agent SDK peers under `agents/` (orchestrator, product, design, architect, implementer, reviewer).

## Prefer

1. Clone this repo and `npx --yes "@grok/agent-sdk@0.4.0" serve --dir ./agents --dev`.
2. Chat with the **orchestrator** only. Give ticket key + stage label.
3. Or mount `@software-factory/core` / `@software-factory/product-skills` in a host agent, and point peer connections at local serve slugs or hosted deploy slugs.

## Stage labels

`prd_draft` → `prd_review` → `design_draft` → `design_review` → `architecture_draft` → `architecture_review` → `implementation` → `pr_review` → `done`

## Do not

- Do not merge the six peers into one mega-agent.
- Do not approve human review gates yourself.
