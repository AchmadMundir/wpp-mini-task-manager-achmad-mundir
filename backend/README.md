# Backend service

Python 3.12, FastAPI, SQLAlchemy, Alembic, and PostgreSQL 16.

## Why this stack

Python is my strongest language and is the language I have used to turn operational rules and data workflows into working internal applications. FastAPI was selected because it keeps request validation and REST contracts explicit while allowing the business rules to remain in plain, independently testable Python services. PostgreSQL was selected because it provides dependable foreign keys, check constraints, transactions, and indexing while matching the team's preferred database.

## Prerequisites

- Python 3.12 (3.11+ works)
- PostgreSQL 16, or Docker Desktop to run PostgreSQL
- `python -m venv` and pip

## Clean setup and run

From `backend/`:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and create local configuration:

```bash
pip install -r requirements-dev.txt
cp .env.example .env
```

From the repository root, start only PostgreSQL:

```bash
docker compose up -d db
```

Return to `backend/`, create the schema, and run the API:

```bash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

The API is available at http://localhost:8000, with Swagger UI at http://localhost:8000/docs.

## Schema creation

Alembic owns schema creation. `alembic upgrade head` applies every migration from an empty database. Do not use `Base.metadata.create_all()` in normal application startup; explicit migrations make the database state reviewable and repeatable.

See [SCHEMA.md](SCHEMA.md) for tables, keys, constraints, indexes, deletion behaviour, and the rejected design alternative.

## Run tests

No web server or database is required for the core service-layer unit tests:

```bash
pytest -v
```

The suite covers successful creation, status filtering, deletion behaviour, empty and whitespace-only values, unknown resources, invalid statuses, and consistent API error bodies.

To additionally verify the real PostgreSQL foreign key, status check, and delete cascade after `alembic upgrade head`:

```bash
# macOS/Linux
TEST_DATABASE_URL=postgresql://task_user:task_password@localhost:5432/task_manager pytest -m integration -v

# Windows PowerShell
$env:TEST_DATABASE_URL="postgresql://task_user:task_password@localhost:5432/task_manager"
pytest -m integration -v
```

Without `TEST_DATABASE_URL`, this database-specific test is reported as skipped while all service and API tests still run.

## Independent-service self-check

With only PostgreSQL and the backend running:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/boards
```

Both commands must return JSON while the frontend is stopped.

## Project layers

```text
app/api             HTTP routes and dependencies
app/services        Business rules with no HTTP concepts
app/repositories    Persistence interfaces and SQLAlchemy implementations
app/models          SQLAlchemy database models
app/schemas         Pydantic request/response contracts
app/core            Configuration, domain errors, and exception handlers
app/db              Engine, session, and declarative metadata
```

## API and error contract

See [API.md](API.md). Every error uses this shape:

```json
{
  "error": "VALIDATION_FAILED",
  "message": "title must not be empty",
  "field": "title"
}
```

`field` is omitted when an error is not associated with one input field.

## Assumptions and trade-offs

- There is one trusted user, so authentication and permissions are not implemented.
- Board names may repeat; uniqueness was not stated and duplicate names can be meaningful in different periods.
- Status is a constrained string rather than a lookup table because the three values are fixed by the brief.
- Board deletion cascades to tasks at the database level. This avoids orphaned tasks and matches the fact that a task belongs to exactly one board.
- Repositories commit individual write operations. A unit-of-work abstraction would be appropriate once use cases span several writes, but it would add unnecessary ceremony to this small application.
- `updated_at` changes when task status changes, which is the only required update operation.

