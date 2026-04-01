#!/usr/bin/env sh
set -eu

DB_HOST="${POSTGRES_SERVER:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-assessment_db}"
DB_USER="${POSTGRES_USER:-postgres}"
DB_PASSWORD="${POSTGRES_PASSWORD:-postgres}"

export PGPASSWORD="$DB_PASSWORD"

# Wait for PostgreSQL before running migrations.
until python - <<'PY'
import os
import psycopg2

host = os.getenv("POSTGRES_SERVER", "postgres")
port = int(os.getenv("POSTGRES_PORT", "5432"))
db = os.getenv("POSTGRES_DB", "assessment_db")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")

conn = psycopg2.connect(host=host, port=port, dbname=db, user=user, password=password)
conn.close()
PY
do
  echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
  sleep 2
done

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Homework & Assessment service..."
exec uvicorn app.main:app --host 0.0.0.0 --port 4002 --reload
