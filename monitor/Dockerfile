# Use official OpenTelemetry Collector base image
FROM otel/opentelemetry-collector:latest

# Set working directory
WORKDIR /otel-config

# Copy your custom configuration into the container
COPY otelcol.yml /etc/otelcol/config.yaml

# Set the command to use the custom config
CMD ["--config=/etc/otelcol/config.yaml"]

