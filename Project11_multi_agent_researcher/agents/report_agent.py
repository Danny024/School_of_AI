import requests

def generate_report(summary: str, corrections: str) -> str:
    prompt = (
        f"Using the summary and fact-check comments below, write a final research brief. "
        f"Incorporate the summary, address any issues raised in the fact-check comments, and ensure the report is concise, professional, and well-structured. "
        f"Use markdown format with clear headings (e.g., ## Overview, ## Key Findings, ## Notes). "
        f"If no issues are raised, use the summary as the basis for the report.\n\n"
        f"Summary:\n{summary}\n\n"
        f"Fact-Check Comments:\n{corrections}"
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()