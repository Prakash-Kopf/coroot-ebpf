from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry import metrics

from prometheus_client import start_http_server

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Setup OTEL Tracer
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "myapp"})
    )
)
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Setup Prometheus Metrics
reader = PrometheusMetricReader()
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))
meter = metrics.get_meter("myapp_meter")
counter = meter.create_counter("myapp_requests", description="App Requests")

# Expose /metrics on port 5000
start_http_server(5000)

@app.route("/")
def index():
    counter.add(1)
    with tracer.start_as_current_span("index-span"):
        return "Hello from instrumented myapp!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

