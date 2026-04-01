# api_gateway

EduSphere API Gateway that provides a single entrypoint for all microservices.

## Architecture

This gateway follows a layered structure:

- `app/routes`: HTTP route registration
- `app/controllers`: request orchestration and response shaping
- `app/services`: proxy forwarding and downstream health checks
- `app/core`: configuration and constants
- `app/schemas`: common response envelope helpers
- `gateway_main.py`: runtime entrypoint

## Integrated Services

Configured gateway prefixes:

- `/identity` -> Identity Service (`4001`)
- `/assessment` -> Homework & Assessment Service (`4002`)
- `/materials` -> Learning Materials Service (`4004`)
- `/monitoring` -> Monitoring & Administration Service (`4007`)
- `/academic` -> Academic Management Service (`4003`)
- `/groups` -> Group Activities Service (`4006`, placeholder)
- `/communication` -> Communication & Student Support Service (`4005`)

## API Gateway Port

- Gateway base URL: `http://localhost:8080`

## Swagger Documentation

- Swagger UI: `http://localhost:8080/docs`
- Swagger UI alias: `http://localhost:8080/api-docs`
- ReDoc: `http://localhost:8080/redoc`
- OpenAPI JSON: `http://localhost:8080/openapi.json`
- OpenAPI JSON alias: `http://localhost:8080/api-docs.json`

## Gateway Endpoints

- `GET /` - gateway metadata
- `GET /health` - gateway health
- `GET /api/v1/gateway/routes` - route registry
- `GET /api/v1/gateway/services/health` - downstream health checks

## Docker Build and Run

1. Copy env template:

```bash
cp .env.example .env
```

2. Build and run:

```bash
docker compose up --build
```

3. Stop:

```bash
docker compose down
```

## Root-Level Orchestration

From repository root, start all integrated services plus gateway with one command:

```bash
docker compose up --build
```

This launches identity, academic, homework-assessment, learning-materials, communication-student-support, monitoring, and api-gateway with their required databases.

## Local Run (without Docker)

```bash
pip install -r gateway_requirements.txt
uvicorn gateway_main:app --reload --port 8080
```

## Postman Collection

Use:

- `EduSphere API Gateway.postman_collection.json`

It includes gateway health/docs checks and example proxied requests for identity, assessment, materials, and monitoring services.
