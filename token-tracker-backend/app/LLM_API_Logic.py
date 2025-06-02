from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import make_asgi_app
from app.observability import metrics
from app.observability.otel import trace
from opentelemetry.trace import format_trace_id
from detoxify import Detoxify
from dotenv import load_dotenv
import time, os, requests


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
model = Detoxify("original")        # create detoxify model
app = FastAPI(debug=False)          # Create app
tracer = trace.get_tracer(__name__) # Create trace

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class ChatRequest(BaseModel):
    user_input: str

class FeedbackRequest(BaseModel):
    user_input: str
    model_output: str
    rating: int
    comment: str = ""

@app.post("/feedback")
async def feedback(data: FeedbackRequest):
    # Store in DB or log for now
    print("Received Feedback:", data.dict())
    return {"status": "Feedbacskssk received"}

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.user_input

    with tracer.start_as_current_span("handle /chat") as parent_span:
        start_time = time.time()

        with tracer.start_as_current_span("groq API call"):
            model_response, prompt_tokens, completion_tokens, model_name, total_time = call_groq_api_with_retry(user_message)

        with tracer.start_as_current_span("toxicity evaluation"):
            toxic_flag, toxic_score = is_toxic(model_response) # Basic toxicity evaluation

        # Calculate latency and record metrics for Prometheus
        latency = time.time() - start_time
        token_total = prompt_tokens + completion_tokens
        metrics.track_tokens(token_total)
        metrics.track_latency_seconds(latency)

        # fetch the current span and trace id
        current_span = trace.get_current_span()
        span_context = current_span.get_span_context()
        trace_id = span_context.trace_id
        formatted_trace_id = format_trace_id(trace_id)

    return {
        "response": model_response,
        "meta": {
            "latency_s": latency,
            "token_usage": {
                "prompt_tokens": prompt_tokens,
                "response_tokens": completion_tokens,
                "total_tokens": token_total
            }
        },
        "model": model_name,
        "trace_id": formatted_trace_id,
        "toxicity_score": toxic_score,
        "flagged_toxic": toxic_flag,
        "total_time": total_time,
    }


def call_groq_api(prompt: str):
    headers = {
        "Authorization": f"Bearer {groq_api_key }",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",  # try llama3 if this fails
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)

    try:
        data = response.json()
        
        return (
            data["choices"][0]["message"]["content"],
            data["usage"]["prompt_tokens"],
            data["usage"]["completion_tokens"],
            data["model"],
            data["usage"]["total_time"]
        )
    except Exception as e:
        print("Groq API parsing error:", e)
        raise

def call_groq_api_with_retry(prompt: str, retries=3):
    for i in range(retries):
        try:
            return call_groq_api(prompt)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2 ** i)
    return "Sorry, something went wrong.", 0, 0, "", 0.0

def is_toxic(text: str) -> tuple[bool, float]:
    scores = model.predict(text)
    toxicity_flag = bool(scores["toxicity"] > 0.7 or scores["insult"] > 0.7 or scores["threat"] > 0.6)
    toxicity_score = float(scores["toxicity"])

    return toxicity_flag, toxicity_score

