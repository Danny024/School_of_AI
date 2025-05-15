# AthenaCore: Multi-Agent AI Collaboration with Persistent Memory
AthenaCore is a multi-agent system that simulates a collaborative think tank. Agents work together on a shared topic, contributing to a persistent memory store and performing specialized tasks.
## Agents
- Research Agent: Finds factual answers
- Summarizer Agent: Condenses knowledge
- Devil’s Advocate Agent: Raises critical flaws
- Insight Agent: Extracts actionable insights
## Features
- Shared memory per topic
- Logs contributions by agent
- Continuity across sessions
## How to Run
1. Pull model: `ollama pull llama2`
2. Start Ollama
3. Run app: `streamlit run frontend.py`