#!/usr/bin/env bash
# Cloud Agent install: Node 22.13+ on the default PATH, then workspace deps.
set -euo pipefail

node -e 'const [maj,min]=process.versions.node.split(".").map(Number); if (maj<22||(maj===22&&min<13)) { console.error("Node 22.13+ required, found "+process.versions.node); process.exit(1); }'
NPM_BIN="$(command -v npm)"
BIN_DIR="$(dirname "$NPM_BIN")"
sudo ln -sfn "$BIN_DIR/node" /usr/local/bin/node
sudo ln -sfn "$BIN_DIR/npm" /usr/local/bin/npm
sudo ln -sfn "$BIN_DIR/npx" /usr/local/bin/npx
npm ci
