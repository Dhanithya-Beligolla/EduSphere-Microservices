# lms_monitoring_service

Monitoring & Administration microservice for EduSphere LMS.

## Overview

This service provides school-level monitoring features:

- Role-based dashboards (Principal, Sectional Head, Class Teacher, Subject Teacher)
- Reports (assignment completion, academic risk, material usage)
- Async report job tracking
- Risk rule management
- Audit trail views
- KPI snapshots and intervention workflow

The service uses PostgreSQL and SQLAlchemy, and runs with Docker.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic v2
- Docker

## Service Ports

- API service: http://localhost:4007
- PostgreSQL host port: 5436

## API Documentation

- Swagger UI (FastAPI): http://localhost:4007/docs
- ReDoc: http://localhost:4007/redoc
- Swagger alias: http://localhost:4007/api-docs
- OpenAPI JSON: http://localhost:4007/api-docs.json

## Environment Configuration

Copy `.env.example` to `.env` and adjust values if needed.

Required variables:

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

## Run with Docker

1. Copy environment file:

```bash
cp .env.example .env
```

2. Start containers:

```bash
docker compose up --build
```

3. Stop containers:

```bash
docker compose down
```

## Main Endpoints

### Service Info

- `GET /`
- `GET /health`

### Dashboards

- `GET /api/v1/dashboards/principal`
- `GET /api/v1/dashboards/sectional-head?sectionId=SEC-JUNIOR`
- `GET /api/v1/dashboards/class-teacher?classId=CLS-G09-A`
- `GET /api/v1/dashboards/subject-teacher?classId=CLS-G09-A&subjectId=SCI`

### Reports

- `GET /api/v1/reports/assignment-completion?termId=TERM-1`
- `GET /api/v1/reports/academic-risk?gradeId=G09`
- `GET /api/v1/reports/material-usage?subjectId=SCI`

### Report Jobs

- `POST /api/v1/report-jobs`
- `GET /api/v1/report-jobs/{jobId}`

### Monitoring Operations

- `GET /api/v1/kpis`
- `GET /api/v1/interventions`
- `PATCH /api/v1/interventions/{interventionId}`
- `GET /api/v1/snapshots`

### Risk and Audit

- `GET /api/v1/risk-rules`
- `POST /api/v1/risk-rules`
- `DELETE /api/v1/risk-rules/{ruleId}`
- `GET /api/v1/audit-views/user-activity?userId=TCH-230`
- `POST /api/v1/audit-views`

## Notes

- The database schema is created at startup.
- Initial seed data is loaded during startup to support dashboard/report responses.
- Responses follow a common envelope: `data`, `meta`, and `errors`.
