from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os
import tiktoken
import time


app = FastAPI()

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
    return {"status": "Feedback received"}

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.user_input
    model_response = call_groq_api_with_retry(user_message)

    # Log token usage
    prompt_tokens = count_tokens(user_message)
    response_tokens = count_tokens(model_response)
    total_tokens = prompt_tokens + response_tokens
    print(f"Token usage: prompt={prompt_tokens}, response={response_tokens}, total={total_tokens}")

    # Basic toxicity evaluation
    toxic = is_toxic(model_response)
    if toxic:
        print("⚠️ Toxic response detected!")

    return {
        "response": model_response,
        "token_usage": {
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": total_tokens
        },
        "toxicity_flag": toxic
    }


def call_groq_api(prompt: str):
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",  # or whichever you're using
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]


def count_tokens(text: str, model: str = "gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def call_groq_api_with_retry(prompt: str, retries=3):
    for i in range(retries):
        try:
            return call_groq_api(prompt)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2 ** i)
    return "Sorry, something went wrong."

def is_toxic(text: str) -> bool:
    # Dummy check — replace with real model
    return "badword" in text.lower()

