# Persistent Memory Agent System
An AI assistant that remembers conversations and research topics across sessions, designed for Athena Research Group. Each topic has its own conversation history and memory, allowing users to continue where they left off, view past interactions, and export session summaries.

## Features
- Topic-specific memory persistence
- Continues where you left off
- Uses LLaMA2 locally via Ollama
- Lightweight memory storage via TinyDB
- Simple Streamlit frontend
## How to Run
1. Pull the model: `ollama pull llama2`
2. Start Ollama
3. Run app: `streamlit run frontend.py`