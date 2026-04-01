#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_ROOT="${SCRIPT_DIR}/.."

CREATE_SUPERUSER=false

if [[ "${1:-}" == "createsuperuser" ]]; then
  CREATE_SUPERUSER=true
fi

cd "${APP_ROOT}"

docker compose build

# Ensure database container is up and accepting connections
docker compose up -d db

echo "Waiting for Postgres to be ready..."
until docker compose exec -T db pg_isready -U "${POSTGRES_USER:-imaging}" >/dev/null 2>&1; do
  sleep 1
done

# Run database migrations against the main stack
docker compose run --rm backend python manage.py migrate

# Reset and repopulate core application data (imaging centers, modalities, insurance)
docker compose run --rm backend python manage.py resetappdata

if [[ "${CREATE_SUPERUSER}" == "true" ]]; then
  docker compose run --rm backend python manage.py createsuperuser
fi

