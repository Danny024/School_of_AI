import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json

app = FastAPI(
    title="Medical Note Structurer",
    description="Extract structured medical data from unstructured clinical notes.",
    version="0.1.0",
)

# Enable CORS for the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:8501")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read Ollama host and port from environment (defaults)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"

class StructuredNote(BaseModel):
    patient_id: str
    symptoms: str
    diagnosis: str
    medications: str
    follow_up: str

class ExtractResponse(BaseModel):
    structured: StructuredNote
    summary: str

@app.get("/health", tags=["health"])
async def health_check():
    """Check if the backend and Ollama service are reachable."""
    try:
        resp = requests.get(f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/tags", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        models = [model["name"] for model in data.get("models", [])]
        if "llama2" not in models:
            return {"status": "warning", "ollama": "reachable", "note": "llama2 model not found"}
        return {"status": "healthy", "ollama": "reachable", "models": models}
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Ollama service unreachable: {str(e)}")

def query_llama(prompt: str) -> str:
    """
    Send a prompt to Ollama LLaMA2 service. Raise HTTPException if any issues.
    Logs full response for debugging.
    """
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": "llama2", "prompt": prompt, "stream": False},
            timeout=15,
        )
        print(f"LLM request sent. Status: {resp.status_code}, Response: {resp.text}")
        resp.raise_for_status()
    except requests.RequestException as e:
        detail = str(e)
        if 'resp' in locals():
            try:
                detail = resp.text
            except:
                pass
        print(f"LLM service error detail: {detail}")
        raise HTTPException(status_code=502, detail=f"LLM service error: {detail}")

    try:
        data = resp.json()
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response: {resp.text}")
        raise HTTPException(status_code=502, detail=f"Invalid LLM response format: {str(e)}")

    if "response" not in data:
        print(f"Unexpected LLM response format: {data}")
        raise HTTPException(status_code=502, detail=f"Unexpected LLM response: {data}")
    return data["response"].strip()

@app.post("/extract/", response_model=ExtractResponse, tags=["extraction"])
async def extract_medical_info(
    patient_id: str = Form(...),
    note: str = Form(...)
):
    # Prompt to extract structured fields
    extraction_prompt = (
        "You are a medical scribe assistant. Extract the following fields from the clinical note:\n"
        "- symptoms\n"
        "- diagnosis\n"
        "- medications\n"
        "- follow_up\n"
        "Return ONLY a JSON object with keys exactly named: symptoms, diagnosis, medications, follow_up.\n\n"
        f"Clinical Note:\n{note}"
    )
    # Prompt to summarize
    summary_prompt = (
        "You are a clinical summarization assistant. Provide a concise one-sentence summary of the case.\n\n"
        f"Clinical Note:\n{note}"
    )

    # Query LLaMA2
    try:
        raw_json = query_llama(extraction_prompt)
        summary_text = query_llama(summary_prompt)
    except HTTPException as e:
        raise e

    # Parse JSON safely
    try:
        structured_data = json.loads(raw_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail=f"Failed to parse JSON: {raw_json}")

    # Validate required fields
    required_fields = {"symptoms", "diagnosis", "medications", "follow_up"}
    if not all(field in structured_data for field in required_fields):
        raise HTTPException(status_code=422, detail="Missing required fields in structured data")

    structured_data["patient_id"] = patient_id

    # Validate StructuredNote model
    try:
        structured_note = StructuredNote(**structured_data)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid structured data: {str(e)}")

    return ExtractResponse(structured=structured_note, summary=summary_text)