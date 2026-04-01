#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${SCRIPT_DIR}/.."

cd "${APP_ROOT}"

# Stop and clean up production-like stack (including nginx)
docker compose down

# Stop and clean up dev stack
docker compose -f docker-compose.dev.yml down

