# Learning Materials Microservice

A production-grade backend microservice for managing digital learning materials in a Sri Lankan school LMS. Built with **FastAPI**, **MongoDB** (Motor async driver), and **Python 3.12**.

## Architecture

```
Route Module → Service Layer → Repository Layer → MongoDB
```

Each layer has a clear responsibility:
- **Routes**: Declare endpoints, validate input via Pydantic, call services, return standard envelopes
- **Services**: Implement business rules, lifecycle transitions, authorization checks, event publishing
- **Repositories**: Isolate MongoDB queries, provide pagination and search

### Project Structure

```
app/
├── main.py                  # FastAPI bootstrap, lifespan, exception handlers
├── core/
│   ├── config.py            # pydantic-settings configuration
│   ├── constants.py         # Enums: Status, ResourceType, Medium, Role
│   ├── dependencies.py      # Auth dependencies (JWT-based)
│   ├── exceptions.py        # Domain-specific exceptions
│   ├── logging.py           # structlog configuration
│   ├── middleware.py         # Correlation ID + request logging
│   └── security.py          # JWT decode + TokenClaims
├── api/
│   ├── router.py            # Central router registry
│   └── routes/
│       ├── health.py        # GET /health, GET /ready
│       ├── materials.py     # CRUD + lifecycle endpoints
│       ├── versions.py      # Version sub-resource
│       ├── visibility.py    # Visibility GET/PATCH
│       ├── download.py      # Download URL stub
│       ├── search.py        # Full-text search
│       ├── analytics.py     # Analytics stub
│       └── ai_tools.py      # AI-assisted endpoints
├── schemas/                 # Pydantic v2 request/response models
├── models/                  # MongoDB document factories
├── services/                # Business logic
├── repositories/            # MongoDB query layer
├── agents/                  # Deterministic AI agents
│   ├── metadata_agent.py    # Tag suggestions, title normalization
│   ├── classification_agent.py  # Resource type classification
│   ├── compliance_agent.py  # Publish readiness checks
│   └── orchestrator.py      # Agent routing
├── events/                  # Domain events + pluggable publisher
│   ├── base.py              # EventPublisher ABC
│   ├── material_events.py   # Typed event factories
│   └── publishers/          # noop + log implementations
├── db/
│   ├── mongo.py             # Motor client lifecycle (lifespan)
│   └── indexes.py           # Index definitions
└── utils/                   # Helpers (pagination, response, ObjectId)

tests/                       # pytest + httpx async tests
scripts/
└── seed.py                  # Sample data seeder
```

## Quick Start

### Prerequisites
- Python 3.12+
- MongoDB 7+ (local or Atlas)

### 1. Clone and install

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env
# Edit .env with your MongoDB URI if needed
```

### 3. Start MongoDB (Docker)

```bash
docker-compose up mongodb -d
```

### 4. Seed sample data

```bash
python -m scripts.seed
```
1. **Identity Service**
   - Handles authentication, authorization, role management, JWT token issuance, and user identity lifecycle.

2. **Academic Management Service**
   - Manages grades, classes, subjects, streams, timetables, and enrollments.

3. **Homework & Assessment Service**
   - Handles assignment creation, submissions, grading, feedback, and result publishing.

4. **Group Activities Service**
   - Supports group projects, memberships, peer evaluation, and shared submissions.

5. **Learning Materials Service**
   - Manages notes, PDFs, videos, links, and learning resources.

6. **Communication & Student Support Service**
   - Handles notices, alerts, messages, and support-related communication.

7. **Monitoring & Administration Service**
   - Provides dashboards, reports, risk indicators, and analytics for school leadership.

8. **API Gateway**
   - Central entry point for routing requests to all services.

### 5. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. View API docs

Open http://localhost:8000/docs (Swagger UI) or http://localhost:8000/redoc (ReDoc)

## Docker

```bash
docker-compose up --build
```

## Running Tests

```bash
pytest tests/ -v
```

## JWT Development Strategy

This service does **not** implement login. It expects a valid JWT Bearer token from an external identity provider. For local development:

### Generate a test token

```python
import jwt
from datetime import datetime, timedelta

token = jwt.encode(
    {
        "sub": "teacher-001",
        "school_id": "school-001",
        "roles": ["SUBJECT_TEACHER"],
        "subject_ids": ["subject-science"],
        "class_ids": ["class-9a"],
        "section_ids": [],
        "stream_ids": [],
        "permissions": [],
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
    },
    "dev-secret-change-in-production",  # Must match JWT_SECRET in .env
    algorithm="HS256",
)
print(token)
```

### Sample curl commands

**Create a material:**
```bash
curl -X POST http://localhost:8000/api/v1/materials \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Grade 9 Science Revision Notes",
    "description": "Complete revision notes for Term 1",
    "resourceType": "PDF",
    "subjectId": "subject-science",
    "gradeId": "grade-9",
    "termId": "term-1",
    "medium": "ENGLISH",
    "tags": ["science", "revision"],
    "fileId": "file-abc-123"
  }'
```

**List materials:**
```bash
curl http://localhost:8000/api/v1/materials \
  -H "Authorization: Bearer <TOKEN>"
```
EduSphere-Microservices/
│
├── api-gateway/
├── identity-service/
├── academic-management-service/
├── homework-assessment-service/
├── group-activities-service/
├── learning-materials-service/
├── communication-student-support-service/
├── monitoring-administration-service/
├── Frontend/
├── docs/
└── README.md
```

## How to Clone the Project

**Publish a material:**
```bash
curl -X POST http://localhost:8000/api/v1/materials/{material_id}/publish \
  -H "Authorization: Bearer <TOKEN>"
```

**Search materials:**
```bash
curl "http://localhost:8000/api/v1/materials/search?q=science&gradeId=grade-9" \
  -H "Authorization: Bearer <TOKEN>"
```

**Suggest tags (AI):**
```bash
curl -X POST http://localhost:8000/api/v1/materials/{material_id}/ai/suggest-tags \
  -H "Authorization: Bearer <TOKEN>"
```

**Health check:**
```bash
curl http://localhost:8000/health
```

## API Response Format

All responses use a consistent envelope:

```json
{
  "data": { ... },
  "meta": {
    "requestId": "uuid",
    "timestamp": "2026-03-29T12:00:00Z",
    "version": "v1"
  },
  "errors": []
}
```

## Authorization Roles

| Role | Create | Read | Update | Publish | Delete |
|------|--------|------|--------|---------|--------|
| ADMIN | ✅ | ✅ | ✅ | ✅ | ✅ |
| PRINCIPAL | ✅ | ✅ | ✅ | ✅ | ✅ |
| DEPUTY_PRINCIPAL | ✅ | ✅ | ✅ | ✅ | ✅ |
| SECTIONAL_HEAD | ✅ | ✅ | ✅ | ✅ | ✅ |
| CLASS_TEACHER | ✅ | ✅ | ✅ | ✅ | ✅ |
| SUBJECT_TEACHER | ✅ (own subjects) | ✅ | ✅ (own subjects) | ✅ | ✅ |
| STUDENT | ❌ | ✅ (published only) | ❌ | ❌ | ❌ |
| PARENT | ❌ | ✅ (published only) | ❌ | ❌ | ❌ |

## Material Lifecycle

```
DRAFT → PUBLISHED → DRAFT (unpublish)
DRAFT → ARCHIVED
PUBLISHED → ARCHIVED
```

## Feature Flags

| Flag | Default | Description |
|------|---------|-------------|
| `ENABLE_AGENT_FEATURES` | `false` | Enable AI-assisted endpoints (tag suggestions, classification) |
| `EVENT_PUBLISHER` | `noop` | Event publisher: `noop` (silent) or `log` (structured logs) |

## Design Decisions

- **Motor** over Beanie: explicit repository pattern, no ORM magic
- **Lifespan** context manager: FastAPI-recommended MongoDB lifecycle
- **PyJWT** stateless parsing: auth server lives elsewhere
- **Deterministic agents**: no LLM dependency, pure Python keyword/rule logic
- **Soft delete**: data safety by default, auditable
- **Pluggable events**: zero coupling, Kafka/RabbitMQ swappable via interface
git clone https://github.com/Dhanithya-Beligolla/EduSphere-Microservices.git
cd EduSphere-Microservices
```

## Example Service Ports
- **API Gateway:** http://localhost:8080
- **Identity Service:** http://localhost:4001
- **Homework & Assessment Service:** http://localhost:4002
- **Group Activities Service:** http://localhost:4003
- **Learning Materials Service:** http://localhost:4004
- **Academic Management Service:** http://localhost:4005
- **Communication & Student Support Service:** http://localhost:4006
- **Monitoring & Administration Service:** http://localhost:4007

## Current Repository Snapshot (Implemented Modules)

The following modules are currently available in this repository:

```bash
EduSphere-Microservices/
│
├── identity-service/
├── homework-assessment-service/
├── EduSphere-Frontend/
└── README.md
```

## Local Development Ports (Current)

For the modules currently implemented in this repository:

- **Identity Service (Docker):** http://localhost:4001
- **Homework & Assessment Service (Docker):** http://localhost:4002
- **Frontend (Vite dev server):** http://localhost:5173

## Quick Start (Current Modules)

Run each module from its own folder in a separate terminal.

### Identity Service

```bash
cd identity-service
cp .env.example .env
docker compose up --build
```

### Homework & Assessment Service

```bash
cd homework-assessment-service
cp .env.example .env
docker compose up --build
```

### EduSphere Frontend

```bash
cd EduSphere-Frontend
npm install
npm run dev
```
