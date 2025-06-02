from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.observability import metrics
from app.observability.otel import trace
from opentelemetry.trace import format_trace_id

import time

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

@app.post("/debug/span")
def observe_spans():
    latency = 0.7
    token_count = 43

    # handles /chat logic
    with tracer.start_as_current_span('handle /debug/span') as parent_span:
        time.sleep(0.1)

        # child span for groq api call
        with tracer.start_as_current_span("simulate LLM call") as llm_call_span:
            time.sleep(0.3)

        # child span for detoxify call
        with tracer.start_as_current_span("simulate toxicity check") as toxicity_span:
            time.sleep(0.2)

        # record metrics for prometheus
        metrics.track_tokens(latency)
        metrics.track_latency_seconds(token_count)

        # fetch the current span and trace id
        current_span = trace.get_current_span()
        span_context = current_span.get_span_context()
        trace_id = span_context.trace_id
        formatted_trace_id = format_trace_id(trace_id)
        
    return {
        "message": "spans recorded",
        "trace_id": formatted_trace_id
    }