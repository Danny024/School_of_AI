from fastapi import FastAPI, Form
import requests

app = FastAPI()

def querry_ollama(prompt: str):
    response = requests.post(
        "http://localhost:1134/api/generate",
        json = {"model" : "mistral", "prompt" : prompt, "stream": False}
    )
    return response.json()["response"].strip()

@app.post("/analyze/")
def analyze_review(text: str = Form(...)):
    sentiment_prompt = f"What is the sentiment (Positive, Neutral, Negative) of the following review?\n\n{text}"
    topic_prompt = f"What is the main issue/topic discussed in this review?\n\n{text}"
    summary_prompt = f"Summarize the review in one short sentence:\n\n{text}"

    sentiment = querry_ollama(sentiment_prompt)
    topic = querry_ollama(topic_prompt)
    summary = querry_ollama(summary_prompt)

    return {"sentiment": sentiment, "topic":topic, "summary": summary}
