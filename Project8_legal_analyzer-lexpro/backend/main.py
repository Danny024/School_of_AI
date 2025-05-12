# from fastapi import FastAPI, Form
# import requests
# app = FastAPI()
# def call_llm(prompt: str):
#     response = requests.post(
#     "http://localhost:11434/api/generate",
#     json={"model": "llama2", "prompt": prompt, "stream": False}
#     )
#     return response.json()["response"].strip()
# @app.post("/analyze/")
# def analyze_legal(text: str = Form(...)):
#     prompts = {
#     "summary": f"Summarize this legal document:\n\n{text}",
#     "clauses": f"Extract key clauses from this legal text (e.g., Terminati
#     "entities": f"Extract all named entities (e.g., parties, locations, dates
#     }
#     results = {k: call_llm(p) for k, p in prompts.items()}
#     return results  

from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Legal Analyzer LexPro",
    description="API for summarizing legal documents, extracting clauses, and named entities.",
    version="0.1.0",
)

class AnalyzeResponse(BaseModel):
    summary: str
    clauses: str
    entities: str


def call_llm(prompt: str) -> str:
    """
    Calls the local Ollama LLM service and returns the generated text.
    Raises HTTPException on errors.
    """
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama2", "prompt": prompt, "stream": False},
            timeout=15,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"LLM service error: {e}")

    data = resp.json()
    if "response" not in data:
        raise HTTPException(status_code=502, detail="Invalid response from LLM.")
    return data["response"].strip()

@app.post("/analyze/", response_model=AnalyzeResponse, tags=["analysis"])
def analyze_legal(text: str = Form(..., description="Full legal document text")):
    """
    Accepts raw legal text and returns:
      - summary
      - key clauses
      - named entities
    """
    # Build prompts
    prompts = {
        "summary": (
            "You are a legal assistant.\n"
            "Summarize the following legal document in concise, clear prose:\n\n" + text
        ),
        "clauses": (
            "You are a legal assistant.\n"
            "Extract and label the key clauses from this document. "
            "Focus on termination, liability, confidentiality, jurisdiction, and any other material terms:\n\n"
            + text
        ),
        "entities": (
            "You are a legal assistant.\n"
            "Identify and list all named entities in the text, including parties, dates, locations, laws, and obligations:\n\n"
            + text
        ),
    }

    # Call LLM for each
    results = {}
    for key, prompt in prompts.items():
        results[key] = call_llm(prompt)

    return AnalyzeResponse(**results)