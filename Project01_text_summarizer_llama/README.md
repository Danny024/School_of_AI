# LLaMA Text Summarizer
This is a simple AI project that uses the LLaMA model (via Ollama) to summarize text.
It has:
- A **FastAPI backend**
- A **Streamlit frontend**
- Local **LLaMA model via Ollama**
## Setup
1. Clone the repo
2. python -m venv venv
3. source venv/bin/activate
4. Install dependencies: `pip install -r requirements.txt`
5. Ru backend: `uvicorn backend.main:app --reload`
6. Run frontend: `streamlit run frontend/app.py`