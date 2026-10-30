#!/usr/bin/env bash
# Cloud Agent start: peer network on 127.0.0.1:3000. Safe to run again.
set -euo pipefail

if curl -sf --max-time 2 http://127.0.0.1:3000/v1/health >/dev/null; then
  echo "software-factory peer network already listening on 127.0.0.1:3000"
  exit 0
fi
exec ./node_modules/.bin/agent-sdk serve --dir ./agents --dev --host 127.0.0.1 --port 3000 --allow-anonymous --allow-anonymous-cursor-account-mcp
