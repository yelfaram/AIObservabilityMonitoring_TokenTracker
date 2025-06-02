from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.observability import metrics
from app.observability.otel import trace

# Create app
app = FastAPI(debug=False)

# Create trace
tracer = trace.get_tracer(__name__)

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/debug/test")
def observe_metrics():
    metrics.track_tokens(43)
    metrics.track_latency_seconds(0.7)
    return {"message": "dummy metrics data fed"}