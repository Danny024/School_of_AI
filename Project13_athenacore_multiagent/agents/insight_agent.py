from .base import call_llm, log_agent_response, get_topic_log

def run(topic: str):
    memory = "\n".join([m["content"] for m in get_topic_log(topic)])
    if not memory:
        return "No content to analyze for insights."
    prompt = f"Extract 2-3 key insights or actionable takeaways from this content:\n\n{memory}"
    insight = call_llm(prompt)
    log_agent_response(topic, "Insight Agent", insight)
    return insight