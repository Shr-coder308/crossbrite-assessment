# Crossbrite Assessment API

Backend assessment project built with FastAPI, PostgreSQL, Redis, Docker, and GitHub Actions.

The API provides authentication, role-based access control, teacher session management, parent-child relationships, and asynchronous evaluation job queuing.

# Tech Stack

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- JWT Authentication
- Docker & Docker Compose
- Pytest
- Ruff
- GitHub Actions

## Architecture

```mermaid
flowchart LR
    Client[Client / Swagger / Postman]
    API[FastAPI Application]
    DB[(PostgreSQL)]
    Redis[(Redis Queue)]

    Client --> API
    API --> DB
    API --> Redis





Core Features
Authentication
JWT-based authentication
Password hashing using Argon2
Protected API endpoints
Active-user validation
Role-Based Access Control
Supported roles:
admin
teacher
parent
student
Teachers can create and access only their own sessions.
Parents can access evaluations only for children linked to their account.
Sessions
Teachers can create sessions containing:
Title
Description
Scheduled time
Status
Teacher ownership
Parent-Child Relationship
Parents can be linked with student accounts.
The API prevents duplicate parent-child relationships.
Evaluations
Teachers can trigger an evaluation for a student.
The evaluation is persisted in PostgreSQL and a job is pushed to Redis.
Example queued job:
{
  "evaluation_id": 2,
  "session_id": 2,
  "status": "queued"
}



The actual LLM evaluation is intentionally mocked/not implemented as permitted by the assessment.
API Documentation
When the application is running, interactive Swagger documentation is available at:
http://localhost:8000/docs
Health check:
http://localhost:8000/health
Running with Docker
Make sure Docker Desktop is running.

Build the application:
      docker compose build

Start all services:
      docker compose up


The application will be available at:
http://localhost:8000
Services:
FastAPI → port 8000
PostgreSQL → port 5432
Redis → port 6379
Database migrations are executed automatically when the API container starts.
Running Tests
Create and activate a Python virtual environment if required, then install dependencies:
          pip install -r requirements.txt

Run the test suite:
     pytest -q
Run linting:
     ruff check .

CI/CD
GitHub Actions runs on pushes and pull requests to main.
The workflow performs:
Dependency installation
Ruff linting
PostgreSQL service startup
Redis service startup
Alembic database migrations
Pytest test suite
Database Migrations
Alembic is used for schema management.
Apply migrations:
alembic upgrade head
Create a new migration:
alembic revision --autogenerate -m "describe change"
Project Structure
       app/
├── api/
│   ├── auth.py
│   ├── sessions.py
│   ├── evaluations.py
│   ├── parent_child.py
│   └── users.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
├── db/
│   └── database.py
├── models/
│   ├── user.py
│   ├── session.py
│   ├── parent_child.py
│   └── evaluation.py
├── schemas/
│   ├── auth.py
│   ├── user.py
│   ├── session.py
│   └── evaluation.py
└── services/
    └── evaluation_service.py

tests/
├── conftest.py
├── test_auth.py
├── test_sessions.py
├── test_rbac.py
└── test_evaluations.py

alembic/
├── versions/
├── env.py
└── script.py.mako

.github/
└── workflows/
    └── ci.yml


Assessment Notes
The current implementation focuses on the requested backend functionality while keeping the evaluation pipeline intentionally lightweight.
For production deployment, secrets should be managed through a secure secret manager, database connections should use appropriate pooling and TLS, Redis should be secured, JWT tokens should have stronger key management and rotation, rate limiting should be added, and structured logging/monitoring should be introduced.
The current Redis queue demonstrates asynchronous job submission. A production implementation would use a dedicated worker system to consume jobs, execute the evaluation, update the evaluation record, and handle retries and failures.


License
This project was created as part of a technical assessment.


1. `README.md` mein paste
2. **Ctrl + S**
3. Terminal:

```powershell
ruff check .