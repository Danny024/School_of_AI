# AI Tutor & Quiz Generator (LearnSphere Academy)
An intelligent assistant for educators and learners to:
- Simplify complex lessons
- Generate quizzes with answers
- Extract key learning concepts
## Tech Stack
- LLM: Mistral via Ollama
- Backend: FastAPI
- Frontend: Streamlit
## How to Run
1. Pull model: `ollama pull mistral`
2. Start backend: `uvicorn backend.main:app --reload`
3. Start frontend: `streamlit run frontend/app.py`