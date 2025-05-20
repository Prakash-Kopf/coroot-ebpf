# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy source
COPY app.py .

# Install dependencies
RUN pip install flask \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-flask \
    opentelemetry-instrumentation-requests \
    opentelemetry-exporter-prometheus \
    prometheus-client

# Expose ports
EXPOSE 5003 8000

# Start app
CMD ["python", "app.py"]

