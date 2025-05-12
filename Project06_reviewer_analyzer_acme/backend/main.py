from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Acme Review Analyzer",
    description="Analyze product reviews: sentiment, topic, and summary.",
    version="0.1.0",
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewAnalysis(BaseModel):
    sentiment: str
    topic: str
    summary: str


def query_ollama(prompt: str) -> str:
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=15,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"LLM service error: {e}")

    data = resp.json()
    if "response" not in data:
        raise HTTPException(status_code=502, detail="Invalid response from LLM.")
    return data["response"].strip()

@app.post("/analyze/", response_model=ReviewAnalysis, tags=["analysis"])
def analyze_review(text: str = Form(..., description="The review text to analyze")):
    sentiment_prompt = (
        "You are a customer feedback analyzer.\n"
        f"Determine the sentiment (Positive, Neutral, Negative) of the following review:\n\n" + text
    )
    topic_prompt = (
        "You are a topic classifier for product reviews.\n"
        f"What is the main issue or topic discussed in this review?\n\n" + text
    )
    summary_prompt = (
        "You are a summarization assistant.\n"
        f"Provide a one-sentence summary of this review:\n\n" + text
    )

    sentiment = query_ollama(sentiment_prompt)
    topic = query_ollama(topic_prompt)
    summary = query_ollama(summary_prompt)

    return ReviewAnalysis(sentiment=sentiment, topic=topic, summary=summary)