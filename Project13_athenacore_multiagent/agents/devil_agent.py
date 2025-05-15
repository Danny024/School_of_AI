from .base import call_llm, log_agent_response, get_topic_log

def run(topic: str):
    memory = "\n".join([m["content"] for m in get_topic_log(topic)])
    if not memory:
        return "No content to challenge."
    prompt = f"Based on the following content, play devil's advocate and raise 2-3 critical counterpoints or potential flaws:\n\n{memory}"
    challenge = call_llm(prompt)
    log_agent_response(topic, "Devil's Advocate", challenge)
    return challenge