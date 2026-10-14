# Mini Task Manager

A small board-based task management application built for the WPP Media Full Stack Developer take-home assessment. The backend and frontend are deliberately separate services and communicate only through a documented REST API.

## Architecture

```text
React/Vite (5173) -> HTTP/JSON -> FastAPI (8000) -> SQLAlchemy -> PostgreSQL (5432)
```

## Quick start with Docker

Prerequisite: Docker Desktop with Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

Windows PowerShell equivalent:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Open:

- Frontend: http://localhost:5173
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Stop all services with `docker compose down`. Data is stored in the named `postgres_data` volume and survives normal container restarts. Use `docker compose down -v` only when you intentionally want an empty database.

## Independent services

Each service has its own dependency manifest, README, and run command:

- [Backend instructions](backend/README.md)
- [Frontend instructions](frontend/README.md)
- [API contract](backend/API.md)
- [Database schema](backend/SCHEMA.md)
- [Indonesian development guide](PANDUAN_PENGERJAAN_ID.md)

The Docker Compose command is a convenience, not a coupling mechanism. The backend can run and answer API calls without the frontend, while the frontend can run without the backend and shows a recoverable connection error.

## Core features

- Create, list, select, and delete boards.
- Create, list, update status, filter, and delete tasks.
- PostgreSQL persistence with Alembic migrations and database constraints.
- Consistent JSON errors and meaningful HTTP status codes.
- Loading, empty, validation, and backend-unavailable states in React.
- Backend service-layer unit tests, plus optional PostgreSQL constraint tests.

## Assumptions

- The application has one trusted user; authentication and authorization are out of scope.
- Board names are not unique because separate projects may legitimately share a name.
- Task results are returned oldest-first for deterministic display.
- Deleting a board permanently deletes its tasks through `ON DELETE CASCADE`.
- Task title and description editing is not implemented because only status editing is required.
- Filtering is performed by the backend through the documented `status` query parameter.

## Trade-offs and unfinished work

- The interface intentionally uses lightweight custom CSS rather than a component library so effort remains focused on correctness, tests, schema design, and documentation.
- The app does not include authentication, audit history, pagination, real-time updates, or cloud deployment because the assessment explicitly excludes them.
- Frontend component tests are not included. Backend business-rule tests were prioritized as requested by the brief.
- Given another week, the next improvements would be a small React test suite for loading and connection-error states, task title/description editing, and a CI check that runs backend tests and the frontend production build.

