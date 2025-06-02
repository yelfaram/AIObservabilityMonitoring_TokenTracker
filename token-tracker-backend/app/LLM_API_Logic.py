from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os
import tiktoken
import time
from dotenv import load_dotenv
from detoxify import Detoxify


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

app = FastAPI()

model = Detoxify("original")

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
    model_response,prompt_tokens,completion_tokens,model, total_time = call_groq_api_with_retry(user_message)

    

    # Basic toxicity evaluation
    toxic_bool, toxic_score = is_toxic(model_response)
    if toxic_bool:
        print("⚠️ Toxic response detected!")

    return {
        "response": model_response,
        "token_usage": {
            "prompt_tokens": prompt_tokens,
            "response_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens
        },
        "toxicity_flag": toxic_bool,
        "toxicity_score": toxic_score,
        "total_time": total_time
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
        print("Groq raw response:\n\n", data)  # 🔍 Print the raw response
        print("This is what youre returning: ", data["choices"][0]["message"]["content"])
        response = data["choices"][0]["message"]["content"]
        prompt_tokens = data["usage"]["prompt_tokens"]
        completion_tokens = data["usage"]["completion_tokens"]
        model = data["model"]
        total_time = data["usage"]["total_time"]

        return response, prompt_tokens,completion_tokens,model, total_time
    except Exception as e:
        print("❌ Error parsing Groq response:", e)
        print("Full response content:", response.text)
        raise



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
    return "Sorry, something went wrong.", 0, 0, "", 0.0

def is_toxic(text: str) -> tuple[bool, float]:
    # # Dummy check — replace with real model
    # return "badword" in text.lower()


   
   
    scores = model.predict(text)
    print("Detoxify scores:", scores)
    print("\ntype of detoxify scores:\n", type(scores))


    toxicity_flag = bool(scores["toxicity"] > 0.7 or scores["insult"] > 0.7 or scores["threat"] > 0.6)
    toxicity_score = float(scores["toxicity"])

    # You can tune these thresholds based on your needs
    return toxicity_flag, toxicity_score

