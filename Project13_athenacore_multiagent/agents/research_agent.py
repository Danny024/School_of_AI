from .base import call_llm, log_agent_response, get_topic_log

def run(topic: str, query: str):
    prompt = f"Research question: {query}\nProvide a concise, factual answer based on available knowledge. Cite key sources or context if relevant."
    answer = call_llm(prompt)
    log_agent_response(topic, "Research Agent", answer)
    return answer