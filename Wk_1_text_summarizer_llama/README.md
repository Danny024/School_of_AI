# LLaMA Text Summarizer
This is a simple AI project that uses the LLaMA model (via Ollama) to summarize text.
It has:
- A **FastAPI backend**
- A **Streamlit frontend**
- Local **LLaMA model via Ollama**
## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run backend: `uvicorn backend.main:app --reload`
4. Run frontend: `streamlit run frontend/app.py`