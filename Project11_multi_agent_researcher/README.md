An intelligent research tool that uses multiple local agents to simulate the research process for Horizon Insights. The system processes a user-provided topic through a pipeline of specialized agents:
- Search Agent
- Summarizer Agent
- Fact Checker Agent
- Report Generator Agent
All powered locally by LLaMA2 via Ollama.
## Run
1. Install Ollama and pull model: `ollama pull llama2`
2. Start backend LLM: `ollama run llama2`
3. Run app: `streamlit run frontend.py`