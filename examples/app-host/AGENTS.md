# app-host

Thin Agent SDK consumer for the software factory. Mounts `@software-factory/core`
and the `plugins/software-factory` Cursor plugin; peers to the orchestrator.

```bash
npm install
npx --yes @grok/agent-sdk@0.4.0 validate --dir .
```

Serve alongside the factory peers, or point `FACTORY_ORCHESTRATOR_SLUG` at a
hosted deploy slug. See [README](./README.md).
