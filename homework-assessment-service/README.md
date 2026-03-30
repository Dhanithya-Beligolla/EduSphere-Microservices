# homework-assessment-service

FastAPI-based Homework & Assessment microservice for the LMS platform.

## MVP Features
- Teacher creates assignments
- Teacher updates assignments
- Teacher publishes assignments
- Student views assignments
- Student submits answers as text and optional file upload
- Teacher views submissions
- Teacher grades submissions
- Teacher publishes results
- Student views results
- Class teacher/admin can view gradebook summary

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- httpx for inter-service calls

## Identity Integration
This service does not handle login directly.
It validates bearer tokens by calling the Identity Service `/api/v1/auth/verify` endpoint.

## Run locally with Docker
1. Copy `.env.example` to `.env`
2. Start the service:
   ```bash
   docker compose up --build
   ```
3. Open docs:
- Swagger UI: `http://localhost:4002/docs`
- ReDoc: `http://localhost:4002/redoc`

## Run migrations
Inside the container or locally:
    ```
    docker exec -it homework-assessment-service alembic upgrade head
    ```
## Main Endpoints
- `POST /api/v1/assignments`
- `GET /api/v1/assignments`
- `GET /api/v1/assignments/{assignment_id}`
- `PATCH /api/v1/assignments/{assignment_id}`
- `POST /api/v1/assignments/{assignment_id}/publish`
- `POST /api/v1/submissions`
- `GET /api/v1/assignments/{assignment_id}/submissions`
- `GET /api/v1/students/{student_id}/submissions`
- `POST /api/v1/submissions/{submission_id}/grade`
- `GET /api/v1/classes/{class_id}/gradebook`
- `POST /api/v1/results/{submission_id}/publish`
- `GET /api/v1/students/{student_id}/results`