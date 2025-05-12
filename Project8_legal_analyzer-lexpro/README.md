# Legal Document Analyzer (LexPro)
AI-powered tool for extracting summaries, key clauses, and named entities from
## Features
- Paste legal contracts or text
- Extract legal clauses (Termination, Liability, etc.)
- Summarize complex documents
- Identify names, dates, places, money
- Streamlit frontend + FastAPI backend
## Usage
1. Pull model: `ollama pull llama2`
2. Run backend: `uvicorn backend.main:app --reload`
3. Run frontend: `streamlit run frontend/app.py