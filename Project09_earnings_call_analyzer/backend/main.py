from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Earnings Call Analyzer",
    description="Analyze earnings call transcripts: summary, sentiment, key insights.",
    version="0.1.0",
)

class AnalysisResponse(BaseModel):
    summary: str
    sentiment: str
    insights: str


def query_model(prompt: str) -> str:
    """
    Sends a prompt to the local Ollama service (Mistral) and returns its response.
    Raises HTTPException on failure.
    """
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=15,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Model service error: {e}")

    data = resp.json()
    if "response" not in data:
        raise HTTPException(status_code=502, detail="Invalid response from model.")
    return data["response"].strip()

@app.post("/analyze/", response_model=AnalysisResponse, tags=["analysis"])
def analyze_call(text: str = Form(..., description="Raw transcript text")):
    """
    Analyze an earnings call transcript and return summary, sentiment, and insights.
    """
    prompts = {
        "summary": (
            "You are a financial analyst.\n"
            "Provide a concise one-paragraph summary of the following earnings call transcript:\n\n" + text
        ),
        "sentiment": (
            "You are a sentiment classifier for financial transcripts.\n"
            "Determine the overall sentiment of the following earnings call (Positive, Neutral, Negative) and justify briefly:\n\n" + text
        ),
        "insights": (
            "You are a financial insights extractor.\n"
            "Extract key financial signals from this earnings call, such as revenue guidance, risk warnings, growth indicators, and strategic actions:\n\n" + text
        ),
    }

    results = {}
    for key, prompt in prompts.items():
        results[key] = query_model(prompt)

    return AnalysisResponse(**results)