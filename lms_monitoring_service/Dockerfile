FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY monitoring_requirements.txt ./
RUN pip install --no-cache-dir -r monitoring_requirements.txt

COPY . /app/lms_monitoring_service

EXPOSE 4007

CMD ["uvicorn", "lms_monitoring_service.monitoring_main:app", "--host", "0.0.0.0", "--port", "4007", "--reload"]
