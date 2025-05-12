import requests

def summarize_text(text: str) -> str:
    prompt = f"Summarize the following findings in 3 bullet points:\n\n{text}"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()