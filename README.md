# Python-cicd — Click Counter

A small hosted web app that counts clicks and saves high scores.

- Web UI: [`app/templates/index.html`](app/templates/index.html)
- API: `POST /api/click`, `POST /api/save`, `GET /api/scores`
- Database: PostgreSQL (Docker Compose, backed by `postgres_data`)

## Features

- Live click counter in the browser
- Save a score with your name (resets the counter)
- Leaderboard of top scores, ordered by score
- Automated tests with pytest
- GitLab CI pipeline: lint, test, build
- GitLab Runner configuration in [`config.toml`](config.toml)

## Tech stack

| Piece | Used |
| --- | --- |
| Web framework | FastAPI |
| Database | PostgreSQL with SQLAlchemy |
| Migrations | Alembic |
| Web server | uvicorn |
| Linting | ruff |
| Tests | pytest + FastAPI TestClient |
| CI | GitLab CI |
| Build | Docker + Compose |

## Getting started

### With Docker (recommended)

Requires Docker and Compose installed.

```sh
docker compose up --build
```

Then open the app at <http://localhost:8000>. The compose stack also starts the PostgreSQL database.

To run migrations:

```sh
docker compose run app alembic upgrade head
```

### Without Docker

1. Copy `.env.example` to `.env` (see [`.env`](.env) for the current values) and adjust the `DATABASE_URL` if you run PostgreSQL yourself.
2. Start the database (for example with `pg_ctl`, Docker, or any PostgreSQL instance).
3. Run migrations:

   ```sh
   alembic upgrade head
   ```

4. Run the app:

   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Tests

```sh
python -m pytest tests
```

Tests use SQLite by default (see `tests/test_main.py`), so they do not require the running PostgreSQL instance.

## GitLab CI

The pipeline in [`.gitlab-ci.yml`](.gitlab-ci.yml) runs three stages:

- **lint** — `ruff check .`
- **test** — `python -m pytest tests`
- **build** — `docker compose build`

## GitLab Runner

The runner used for this project is configured in [`config.toml`](config.toml). Key settings:

- `executor = "docker"` — jobs run in containers against the local Docker socket
- `request_concurrency = 3` — allows multiple simultaneous job requests (long-polling friendly)
- `concurrent = 4` — up to 4 jobs in parallel across the runner
