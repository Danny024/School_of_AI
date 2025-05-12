 # Code Review Assistant (DeepSeek-Coder)

    This tool uses the **DeepSeek-Coder model** via Ollama to analyze code and provide feedback, suggestions, or bug fixes.

    ## Features
    - FastAPI backend
    - Streamlit frontend
    - Locally hosted DeepSeek-Coder via Ollama

    ## How to Run
    1. Pull model: `ollama pull deepseek-coder`
    2. Start backend: `uvicorn backend.main:app --reload`
    3. Start frontend: `streamlit run frontend/app.py`
    4. Paste your code and get helpful feedback!