from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="AI Tutor & Quiz Generator",
    description="Generates simplified explanations, quizzes, and concept lists from educational text.",
    version="0.1.0",
)

class LearningAids(BaseModel):
    explanation: str
    quiz: str
    concepts: str


def query_model(prompt: str) -> str:
    """
    Send a prompt to the local Ollama LLM service and return the response text.
    Raises HTTPException on communication errors or malformed responses.
    """
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

@app.post("/generate/", response_model=LearningAids, tags=["generation"])
def generate_learning_aids(text: str = Form(..., description="Educational text to process")):
    """
    Generate simplified explanation, quiz questions, and key concepts from input text.
    """
    # Build prompts for each task
    prompts = {
        "explanation": (
            "You are an AI tutor. Explain the following content in simple, student-friendly language:\n\n" + text
        ),
        "quiz": (
            "You are an AI educator. Create 5 quiz questions (multiple-choice or short answer) with correct answers based on this content:\n\n" + text
        ),
        "concepts": (
            "You are a study assistant. List 5 to 10 key terms or concepts from the following text for revision:\n\n" + text
        ),
    }

    # Query the model for each
    results = {}
    for key, prompt in prompts.items():
        results[key] = query_model(prompt)

    return LearningAids(**results)