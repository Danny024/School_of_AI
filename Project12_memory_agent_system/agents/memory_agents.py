import requests
from tinydb import TinyDB, Query

db = TinyDB('memory/memory_store.json')
Topic = Query()

def call_llama(prompt: str) -> str:
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    return res.json()["response"].strip()

def get_topic_history(topic: str):
    result = db.search(Topic.name == topic)
    return result[0]["messages"] if result else []

def update_memory(topic: str, user_msg: str, ai_msg: str):
    if db.contains(Topic.name == topic):
        db.update(lambda t: t["messages"].append({"user": user_msg, "ai": ai_msg}), Topic.name == topic)
    else:
        db.insert({"name": topic, "messages": [{"user": user_msg, "ai": ai_msg}]})

def run_agent(topic: str, user_input: str) -> str:
    history = get_topic_history(topic)
    memory_context = "\n".join([f"User: {m['user']}\nAI: {m['ai']}" for m in history])
    prompt = f"{memory_context}\nUser: {user_input}\nAI:"
    ai_reply = call_llama(prompt)
    update_memory(topic, user_input, ai_reply)
    return ai_reply