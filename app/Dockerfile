FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install flask \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-exporter-prometheus \
    opentelemetry-instrumentation-flask \
    prometheus_client

CMD ["python", "app.py"]

