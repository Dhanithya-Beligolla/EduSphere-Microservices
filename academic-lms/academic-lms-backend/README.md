# Academic LMS Backend Service

Academic LMS Backend manages core academic structures such as academic years, grades, sections, subjects, enrollments, teacher assignments, and timetable operations.

## Tech Stack

- Node.js + Express
- MongoDB + Mongoose
- Swagger (swagger-jsdoc + swagger-ui-express)
- Docker

## Service Port

- API base URL: http://localhost:4003
- Health endpoint: http://localhost:4003/api/health
- Swagger docs: http://localhost:4003/api-docs

## Main API Prefix

- `/api`

## Key Endpoints

### Academic Years
- `GET /api/academic-years`
- `GET /api/academic-years/active`
- `POST /api/academic-years`
- `PATCH /api/academic-years/:id/activate`
- `DELETE /api/academic-years/:id`

### Grades and Sections
- `GET /api/grades`
- `POST /api/grades`
- `PUT /api/grades/:id`
- `DELETE /api/grades/:id`
- `GET /api/sections`
- `POST /api/sections`
- `PUT /api/sections/:id`
- `DELETE /api/sections/:id`

### Subjects
- `GET /api/subjects`
- `GET /api/subjects/:id`
- `POST /api/subjects`
- `PUT /api/subjects/:id`
- `DELETE /api/subjects/:id`

### Enrollments
- `GET /api/enrollments`
- `GET /api/enrollments/student/:studentId`
- `POST /api/enrollments`
- `PATCH /api/enrollments/:id/transfer`
- `POST /api/enrollments/promote`

### Teacher Assignments and Timetable
- `GET /api/teacher-assignments`
- `GET /api/teacher-assignments/teaching-load/:teacherId`
- `POST /api/teacher-assignments`
- `DELETE /api/teacher-assignments/:id`
- `GET /api/timetable`
- `POST /api/timetable`
- `POST /api/timetable/bulk`
- `PUT /api/timetable/:id`
- `DELETE /api/timetable/:id`
- `POST /api/timetable/publish`

## Local Run (Docker)

1. Optional: create env file (defaults are provided in compose):

```bash
cp .env.example .env
```

2. Start the service and its MongoDB container:

```bash
docker compose up --build
```

3. Stop containers:

```bash
docker compose down
```

## Build Docker Image Only

```bash
docker build -t edusphere-academic-lms:latest .
```

## Notes

- Required env values are documented in `.env.example`.
- Standalone compose automatically provisions MongoDB and defaults `MONGO_URI` to `mongodb://mongodb:27017/academic_lms`.
