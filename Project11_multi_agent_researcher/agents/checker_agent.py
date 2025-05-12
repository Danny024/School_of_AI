import requests

def fact_check(text: str) -> str:
    prompt = (
        f"Check the following summary for bias, hallucination, or inaccuracies. "
        f"Identify any issues and suggest improvements. If no issues are found, state that the summary is accurate. "
        f"Return the response in a clear, concise format.\n\n"
        f"Summary:\n{text}"
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()