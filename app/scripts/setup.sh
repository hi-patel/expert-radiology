#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${SCRIPT_DIR}/.."

cd "${APP_ROOT}"

docker compose -f docker-compose.dev.yml build
docker compose build

# Run database migrations inside the dev backend container so tables exist for both stacks
docker compose -f docker-compose.dev.yml run --rm backend python manage.py migrate


