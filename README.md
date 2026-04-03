# EduSphere-Microservices

EduSphere is a school LMS platform implemented as domain-oriented microservices. This repository includes the active backend modules, their data stores, and a centralized API gateway.

The current snapshot focuses on seven operational services:

- Identity Service
- Academic Management Service
- Homework and Assessment Service
- Learning Materials Service
- Communication and Student Support Service
- Monitoring and Administration Service
- API Gateway

## Vision and Scope

EduSphere is designed to support core school workflows:

- User identity, access control, and role-based permissions
- Assignment lifecycle from creation to result publication
- Digital content management for teaching and learning
- Monitoring dashboards and administration analytics
- Unified access via a single gateway entry point

The architecture is service-first so each domain can evolve independently while still integrating through common API contracts.

## High-Level Architecture

```text
Clients (Web / Mobile / Admin)
            |
            v
       API Gateway :8080
/identity /academic /assessment /materials /communication /monitoring
    |         |         |           |            |               |
    v         v         v           v            v               v
Identity   Academic   Homework    Learning   Communication   Monitoring
Service    Service    Service     Materials  Service         Service
:4001      :4003      :4002       :4004      :4005           :4007
   |          |          |            |                          |
   v          v          v            v                          v
Postgres    MongoDB    Postgres     MongoDB                    Postgres
:5433       :27017     :5434        :27017                     :5436
```

## Service Catalog

### 1. Identity Service

- Purpose: authentication, JWT issuance, authorization support, and user lifecycle controls.
- Stack: Node.js, Express, Sequelize, PostgreSQL.
- Key capabilities:
  - Login and token issuance
  - User registration and status updates
  - Token verification endpoint for downstream services
  - Seeded super admin bootstrap
- Details: [identity-service/README.md](identity-service/README.md)

### 2. Academic Management Service

- Purpose: manage academic years, grades, sections, subjects, enrollments, teacher assignments, and timetables.
- Stack: Node.js, Express, MongoDB.
- Key capabilities:
  - Academic year lifecycle management
  - Grade and section operations
  - Subject and timetable management
  - Student enrollment and promotion workflows
  - Teacher assignment management
- Details: [academic-lms/backend/README.md](academic-lms/backend/README.md)

### 3. Homework and Assessment Service

- Purpose: manage assignments, submissions, grading, and result publication.
- Stack: FastAPI, SQLAlchemy, Alembic, PostgreSQL.
- Key capabilities:
  - Assignment create, update, publish
  - Student submission flows with optional file uploads
  - Teacher grading and result publication
  - Gradebook summary views
  - Identity token validation integration
- Details: [homework-assessment-service/README.md](homework-assessment-service/README.md)

### 4. Learning Materials Service

- Purpose: manage learning resources such as notes, PDFs, links, and media.
- Stack: FastAPI, Motor, MongoDB, Pydantic v2.
- Key capabilities:
  - Material CRUD and lifecycle management
  - Subject and grade-aware organization
  - Search and visibility management
  - AI-assisted metadata and tag suggestion endpoints
- Details: [Learning-Materials/README.md](Learning-Materials/README.md)

### 5. Communication and Student Support Service

- Purpose: handle notices, student-teacher messaging, alerts, and support/counselling cases.
- Stack: FastAPI, Pydantic.
- Key capabilities:
  - Notice create/list/publish flows
  - Conversation messaging endpoints
  - User alert management
  - Support case creation and updates
- Details: [communication-student-support-service/README.md](communication-student-support-service/README.md)

### 6. Monitoring and Administration Service

- Purpose: provide school leadership dashboards, KPIs, reports, and audit views.
- Stack: FastAPI, SQLAlchemy, PostgreSQL.
- Key capabilities:
  - Principal, sectional head, class teacher, subject teacher dashboards
  - Academic risk and material usage reporting
  - Report jobs and intervention tracking
  - Audit and risk-rule workflows
- Details: [lms_monitoring_service/README.md](lms_monitoring_service/README.md)

### 7. API Gateway

- Purpose: single entry point for routing requests to backend services.
- Stack: FastAPI, httpx.
- Key capabilities:
  - Prefix-based routing to downstream services
  - Centralized service registry
  - Gateway and downstream health checks
  - Unified API docs exposure
- Details: [api_gateway/README.md](api_gateway/README.md)

## Port and Endpoint Matrix

| Component | Internal Purpose | Host Port | Health / Docs |
|---|---|---:|---|
| API Gateway | Unified entry point | 8080 | /health, /api-docs |
| Identity Service | Auth and users | 4001 | /health, /api-docs |
| Academic Management | Academic domain workflows | 4003 | /api/health, /api-docs |
| Homework and Assessment | Assignment workflows | 4002 | /health, /docs |
| Learning Materials | Learning content management | 4004 | /health, /docs |
| Communication and Student Support | Notices, messaging, support workflows | 4005 | /health, /docs |
| Monitoring and Administration | Dashboards and reporting | 4007 | /health, /api-docs |
| Identity PostgreSQL | Identity datastore | 5433 | n/a |
| Assessment PostgreSQL | Assessment datastore | 5434 | n/a |
| Monitoring PostgreSQL | Monitoring datastore | 5436 | n/a |
| MongoDB | Materials datastore | 27017 | n/a |

## API Documentation Quick Links

- Gateway Swagger: http://localhost:8080/api-docs
- Gateway OpenAPI: http://localhost:8080/api-docs.json
- Identity Swagger: http://localhost:4001/api-docs
- Academic Swagger: http://localhost:4003/api-docs
- Homework Swagger: http://localhost:4002/docs
- Learning Materials Swagger: http://localhost:4004/docs
- Communication Swagger: http://localhost:4005/docs
- Monitoring Swagger: http://localhost:4007/api-docs

## Root-Level Orchestration

This repository includes a root orchestration file at [docker-compose.yml](docker-compose.yml) that runs all active services and required databases.

### Start all services

```bash
docker compose up --build
```

### Stop all services

```bash
docker compose down
```

### Run in detached mode

```bash
docker compose up --build -d
```

### View running containers

```bash
docker compose ps
```

### View logs

```bash
docker compose logs -f
```

## Full Microservice Run (Verified)

Use this flow to run the entire platform from a clean state.

### 1. Clean previous conflicting containers (safe for this repo stack)

```bash
docker rm -f identity-postgres assessment-postgres monitoring-postgres lms-mongodb identity-service homework-assessment-service lms-learning-materials academic-lms-backend communication-student-support-service lms-monitoring-service lms-api-gateway 2>/dev/null || true
```

### 2. Build and start all services

```bash
docker compose up -d --build
```

### 3. Verify all health endpoints through API Gateway

```bash
curl http://localhost:8080/health
curl http://localhost:8080/identity/health
curl http://localhost:8080/assessment/health
curl http://localhost:8080/materials/health
curl http://localhost:8080/communication/health
curl http://localhost:8080/monitoring/health
curl http://localhost:8080/academic/api/health
```

Expected result: each endpoint should return `200 OK`.

### 4. Verify aggregated downstream status

```bash
curl http://localhost:8080/api/v1/gateway/services/health
```

Notes:
- Active services should report `UP`.
- `groups` can report `DOWN` in this repository because it is a reserved gateway route without an implemented backend service.

### 5. Stop the full stack

```bash
docker compose down
```

## Per-Service Development

Each service can still be run independently for focused development.

- Identity: [identity-service/README.md](identity-service/README.md)
- Academic: [academic-lms/academic-lms-backend/README.md](academic-lms/academic-lms-backend/README.md)
- Homework and Assessment: [homework-assessment-service/README.md](homework-assessment-service/README.md)
- Learning Materials: [Learning-Materials/README.md](Learning-Materials/README.md)
- Communication and Student Support: [communication-student-support-service/README.md](communication-student-support-service/README.md)
- Monitoring: [lms_monitoring_service/README.md](lms_monitoring_service/README.md)
- Gateway: [api_gateway/README.md](api_gateway/README.md)

## Data and Storage Strategy

- Service-owned datastores are isolated by domain.
- Relational domains use PostgreSQL.
- Content-heavy learning materials use MongoDB.
- This separation reduces coupling and allows domain-specific optimization.

## Security and Integration Notes

- JWT validation is centralized through the Identity service.
- Homework service validates bearer tokens using Identity verification endpoints.
- Academic service uses MongoDB-backed domain models for academic entities.
- Communication service currently uses in-memory mock storage for rapid prototyping.
- Gateway forwards requests and supports service health visibility.
- In production, replace development secrets and tighten CORS and network policies.

## Current Module Status

Active and integrated in this repository:

- Identity Service
- Academic Management Service
- Homework and Assessment Service
- Learning Materials Service
- Communication and Student Support Service
- Monitoring and Administration Service
- API Gateway

Reserved in gateway routing but not currently implemented as backend modules in this repository:

- Group Activities Service

## Repository Structure

```text
EduSphere-Microservices/
├── identity-service/
├── academic-lms/
├── homework-assessment-service/
├── Learning-Materials/
├── communication-student-support-service/
├── lms_monitoring_service/
├── api_gateway/
├── EduSphere-Frontend/
├── docker-compose.yml
└── README.md
```

## Suggested Verification Checklist

After startup, verify the platform quickly:

1. Open gateway docs at http://localhost:8080/api-docs
2. Check gateway health at http://localhost:8080/health
3. Check service docs on ports 4001, 4002, 4003, 4004, 4005, and 4007
4. Run gateway downstream health route at:
   - http://localhost:8080/api/v1/gateway/services/health

## License

See [LICENSE](LICENSE).
