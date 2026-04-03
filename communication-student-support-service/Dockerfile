FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY communication_requirements.txt ./
RUN pip install --no-cache-dir -r communication_requirements.txt

COPY . .

EXPOSE 4005

CMD ["uvicorn", "communication_main:app", "--host", "0.0.0.0", "--port", "4005", "--reload"]
