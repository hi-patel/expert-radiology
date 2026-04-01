# expert-radiology
Imaging Directory App for expert radiology

# Initial Setup

Before you start, make sure the following are installed locally:
- **Docker Desktop** (or Docker Engine) with Docker Compose support

From the repo root, run the setup script once to build containers, run migrations, and seed mock data (modalities, insurance plans, and imaging centers).

```bash
cd app
bash scripts/setup.sh
```

This will also reset and re-seed app data each time you run it.

# Run the app
From the repo root:

```bash
cd app
bash scripts/start.sh
```

This single script starts:

- Postgres + Django backend
- Next.js dev server for the frontend
- nginx proxy

Then open:

- Frontend UI: `http://localhost:3000`

### Troubleshooting

If you see the following error, wait a few minutes and try setup.sh again.
```bash
django.db.utils.OperationalError: connection to server at "db" (172.21.0.2), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

# Product Roadmap
[Roadmap.md](/product/ROADMAP.md)
