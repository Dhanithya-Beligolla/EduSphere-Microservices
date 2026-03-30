# identity-service

Identity and user management microservice for the LMS platform.

## Features
- Super admin bootstrap
- Role-based user registration
- Login with JWT
- Authenticated current user endpoint
- Token verification endpoint for other microservices
- PostgreSQL with Sequelize
- Dockerized local development

## Run with Docker
1. Copy `.env.example` to `.env`

2. Start the containers:
   ```bash
   docker compose up --build
   ```
3. Service runs at:
- API: `http://localhost:4001`

- Health: `http://localhost:4001/health`

## Run without Docker

1. Install dependencies:
    ```bash
    npm install
    ```
2. Set up PostgreSQL and update `.env`

3. Start dev server:
    ```bash
    npm run dev
    ```


## Default seeded super admin

- username: `superadmin`

- email: `superadmin@lms.com`

- password: `Super@12345`

## Main endpoints

- `POST /api/v1/auth/login`

- `POST /api/v1/auth/register`

- `GET /api/v1/auth/me`

- `GET /api/v1/auth/verify`

- `GET /api/v1/auth/users`

- `GET /api/v1/auth/users/:id`

- `PATCH /api/v1/auth/users/:id/status`