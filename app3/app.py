from flask import Flask, request
from prometheus_client import start_http_server, Counter, Histogram
import time, random

# OTEL
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Resource with service name
resource = Resource.create({"service.name": "coroot-demo-cloud"})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Exporter with API Key & OTLP HTTP endpoint
otlp_exporter = OTLPSpanExporter(
    endpoint="http://135.13.28.200:30602/v1/traces",
    headers={"x-api-key": "nkUONsnlfXKKopo4kfN_fsh2RdB15aKa"},
    
)

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Metrics setup
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["endpoint"])

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

@app.route("/")
def index():
    with tracer.start_as_current_span("index"):
        time.sleep(random.uniform(0.1, 0.3))
        return "Hello from Coroot Demo (Cloud)!"

@app.route("/login")
def login():
    with tracer.start_as_current_span("login"):
        time.sleep(random.uniform(0.1, 0.2))
        return "Login Page"

@app.route("/checkout")
def checkout():
    with tracer.start_as_current_span("checkout"):
        time.sleep(random.uniform(0.2, 0.4))
        return "Checkout Page"

@app.route("/profile")
def profile():
    with tracer.start_as_current_span("profile"):
        time.sleep(random.uniform(0.1, 0.2))
        return "User Profile"

@app.route("/search")
def search():
    with tracer.start_as_current_span("search"):
        time.sleep(random.uniform(0.05, 0.15))
        return "Search Page"

if __name__ == "__main__":
    start_http_server(8000)
    app.run(host="0.0.0.0", port=5003)

