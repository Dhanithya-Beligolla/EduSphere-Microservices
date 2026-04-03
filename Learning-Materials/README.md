# Learning-Materials Service

Learning Materials Service manages digital resources (notes, PDFs, videos, links, and AI-assisted metadata) used by students and teachers.

## Responsibilities

- Material CRUD and lifecycle management
- Subject/grade/term-based organization
- Search, filtering, and visibility controls
- Versioning and download workflow hooks
- AI helper endpoints for tag and metadata suggestions

## Tech Stack

- FastAPI
- MongoDB (Motor async driver)
- Pydantic v2
- Uvicorn

## Service Endpoints

- Base URL: http://localhost:4004
- Health: http://localhost:4004/health
- Swagger: http://localhost:4004/docs
- ReDoc: http://localhost:4004/redoc

## Local Run (Docker)

```bash
cp .env.example .env
docker compose up --build
```

## Notes

- Keep `MONGO_URI` aligned with runtime mode:
  - Standalone compose: `mongodb://mongodb:27017`
  - Root-level orchestration: also `mongodb://mongodb:27017` via service networking
