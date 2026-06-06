import os
import time
import requests
from dotenv import load_dotenv
from flask import Flask, g, request, abort
from prometheus_client import Counter, generate_latest, REGISTRY, Histogram

# OpenTelemetry
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

load_dotenv()

app = Flask(__name__)

# ---------- OpenTelemetry Tracing ----------
resource = Resource(attributes={SERVICE_NAME: "my-flask-app"})
trace.set_tracer_provider(TracerProvider(resource=resource))

otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# ---------- Prometheus metrics ----------
VISITS = Counter('app_visits_total', 'Total number of visits')
REQUEST_TIME = Histogram(
    'app_request_duration_seconds',
    'Request duration',
    labelnames=['method', 'endpoint']
)

# Internal/loopback IPs allowed to scrape /metrics
METRICS_ALLOWED_HOSTS = {'127.0.0.1', '::1', 'prometheus'}

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        endpoint = request.endpoint if request.endpoint else 'unknown'
        REQUEST_TIME.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)
    return response

@app.route('/metrics')
def metrics():
    client_ip = request.remote_addr
    if client_ip not in METRICS_ALLOWED_HOSTS:
        abort(403)
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain'}

@app.route('/')
def hello_world():
    return 'Hello, I\'m Vitalii Davydov - SRE candidate'

@app.route('/health')
def health_check():
    return {"status": "ok"}, 200

@app.route('/version')
def get_version():
    return {"version": os.getenv('APP_VERSION')}

@app.route('/outbound')
def outbound():
    requests.get("https://httpbin.org/status/200")
    return "Outbound call done"
