from agents.memory_agents import run_agent, get_topic_history

def handle_query(topic: str, user_input: str):
    response = run_agent(topic, user_input)
    history = get_topic_history(topic)
    return response, history