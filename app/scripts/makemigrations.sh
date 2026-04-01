#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${SCRIPT_DIR}/.."

cd "${APP_ROOT}"

# Run makemigrations inside the backend container so migration files are written to the local filesystem
docker compose run --rm backend python manage.py makemigrations

