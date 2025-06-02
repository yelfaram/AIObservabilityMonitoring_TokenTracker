from prometheus_client import Counter, Histogram

# Define which metrics you want to track that Prometheus will monitor

# Counter: track cumulative token usage
chat_token_usage_total = Counter(
    'chat_token_usage_total', 
    'Track total number of LLM tokens used by /chat endpoint'
)

# histogram: track cumulative token usage
chat_request_latency_seconds = Histogram(
    'chat_request_latency_seconds', 
    'Track request latency in seconds for /chat endpoint'
)

# Helpers (to be called from routes to update metrics)
def track_tokens(tokens: int = 1):
    chat_token_usage_total.inc(tokens)

def track_latency_seconds(latency: float):
    chat_request_latency_seconds.observe(latency)