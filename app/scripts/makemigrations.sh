#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${SCRIPT_DIR}/.."

cd "${APP_ROOT}"

# Run makemigrations inside the dev backend container so migration files are written to the local filesystem
docker compose -f docker-compose.dev.yml run --rm backend python manage.py makemigrations

