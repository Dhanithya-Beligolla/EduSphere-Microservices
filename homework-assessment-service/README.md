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
- httpx

## Service Ports

- API service: http://localhost:4002
- PostgreSQL host port: 5434

## API Documentation

- Swagger UI: http://localhost:4002/docs
- ReDoc: http://localhost:4002/redoc
- OpenAPI JSON: http://localhost:4002/openapi.json

## Health Check

- `GET /health`

## Environment Configuration

Copy `.env.example` to `.env` and update values if needed.

Important variables:

- `APP_NAME`
- `APP_ENV`
- `API_V1_PREFIX`
- `PORT`
- `POSTGRES_SERVER`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DATABASE_URL` (optional override)
- `IDENTITY_SERVICE_BASE_URL`
- `IDENTITY_VERIFY_ENDPOINT`
- `ACADEMIC_SERVICE_BASE_URL`
- `UPLOAD_DIR`
- `MAX_FILE_SIZE_MB`

## Identity Integration

This service does not perform login directly.
It validates bearer tokens via the Identity Service verification endpoint.

## Run locally with Docker
1. Copy `.env.example` to `.env`
2. Start the service:
   ```bash
   docker compose up --build
   ```
3. Open docs:
- Swagger UI: `http://localhost:4002/docs`
- ReDoc: `http://localhost:4002/redoc`

## Database Migrations

Migrations now run automatically when the service container starts.

Manual migration command (optional):

```bash
docker exec -it homework-assessment-service alembic upgrade head
```

## Main Endpoints

### Assignments

- `POST /api/v1/assignments`
- `GET /api/v1/assignments`
- `GET /api/v1/assignments/{assignment_id}`
- `PATCH /api/v1/assignments/{assignment_id}`
- `POST /api/v1/assignments/{assignment_id}/publish`

### Submissions

- `POST /api/v1/submissions`
- `GET /api/v1/assignments/{assignment_id}/submissions`
- `GET /api/v1/students/{student_id}/submissions`

### Grading and Results

- `POST /api/v1/submissions/{submission_id}/grade`
- `POST /api/v1/results/{submission_id}/publish`
- `GET /api/v1/students/{student_id}/results`
- `GET /api/v1/classes/{class_id}/gradebook`

## Notes

- Uploads are served from `/uploads` and stored in the configured upload directory.
- Keep the identity service running for token verification flows.