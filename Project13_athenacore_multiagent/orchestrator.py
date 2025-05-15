from agents import research_agent, summarizer_agent, devil_agent, insight_agent

def run_agent(agent: str, topic: str, query: str = ""):
    try:
        if agent == "Research":
            if not query:
                return "Research Agent requires a query."
            return research_agent.run(topic, query)
        elif agent == "Summarizer":
            return summarizer_agent.run(topic)
        elif agent == "Devil":
            return devil_agent.run(topic)
        elif agent == "Insight":
            return insight_agent.run(topic)
        else:
            return "Unknown agent."
    except Exception as e:
        return f"Error running {agent} Agent: {str(e)}"