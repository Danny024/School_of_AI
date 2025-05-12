from fastapi import FastAPI, Form
import requests
import re
import json

app = FastAPI()

def query_llama(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    raw_response = response.json()["response"].strip()
    # Extract JSON part using regex
    json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        # Validate and return JSON
        try:
            json.loads(json_str)  # Ensure it's valid JSON
            return json_str
        except json.JSONDecodeError:
            return '{"symptoms": "N/A", "diagnosis": "N/A", "medications": "N/A", "follow_up": "N/A"}'
    return '{"symptoms": "N/A", "diagnosis": "N/A", "medications": "N/A", "follow_up": "N/A"}'

@app.post("/extract/")
def extract_medical_info(note: str = Form(...)):
    prompt = (
        f"Extract the following from the doctor's note and return in JSON format:\n"
        f"- Symptoms\n- Diagnosis\n- Medications\n- Follow-up Instructions\n"
        f"Ensure the output is valid JSON, e.g., {{\"symptoms\": \"\", \"diagnosis\": \"\", \"medications\": \"\", \"follow_up\": \"\"}}.\n"
        f"Do not include any additional text or explanations outside the JSON.\n\n"
        f"Note:\n{note}"
    )
    structured_data = query_llama(prompt)
    return {"structured": structured_data}