from flask import Flask, request
from prometheus_client import start_http_server, Counter
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Set up tracing
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({"service.name": "flask-demo"}))
)

# Set up an OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://192.168.1.39:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Set up the Flask app
app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

# Set up Prometheus metrics
start_http_server(8000)
REQUEST_COUNTER = Counter("http_requests_total", "Total HTTP requests")

@app.route("/")
def hello():
    REQUEST_COUNTER.inc()
    return "Hello, OpenTelemetry with Python!"

@app.route("/process")
def process():
    REQUEST_COUNTER.inc()
    # Simulate some processing
    return "Processing complete!"

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False)

