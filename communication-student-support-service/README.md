# Communication Student Support Service

Communication & Student Support Service handles notices, direct messaging, alerts, and support/counselling case workflows.

## Tech Stack

- FastAPI
- Pydantic v2
- Uvicorn
- Docker

## Service Port

- API base URL: http://localhost:4005
- Health endpoint: http://localhost:4005/health
- Swagger docs: http://localhost:4005/docs
- ReDoc: http://localhost:4005/redoc

## Main API Prefix

- `/api/v1`

## Key Endpoints

### Notices
- `POST /api/v1/notices`
- `GET /api/v1/notices`
- `POST /api/v1/notices/{noticeId}/publish`

### Messages
- `POST /api/v1/messages`
- `GET /api/v1/conversations/{conversationId}/messages`

### Alerts
- `POST /api/v1/alerts`
- `GET /api/v1/users/{userId}/alerts`

### Support Cases
- `POST /api/v1/support-cases`
- `GET /api/v1/support-cases/{caseId}`
- `PATCH /api/v1/support-cases/{caseId}`

## Local Run (Docker)

1. Create env file:

```bash
cp .env.example .env
```

2. Start service:

```bash
docker compose up --build
```

## Build Docker Image Only

```bash
docker build -t edusphere-communication-support:latest .
```

## Notes

- This implementation uses in-memory mock data.
- Data resets when the service restarts.
