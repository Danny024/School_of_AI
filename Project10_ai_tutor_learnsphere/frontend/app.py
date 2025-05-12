import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Tutor & Quiz Generator", layout="wide")
st.title("📚 AI Tutor & Quiz Generator for LearnSphere Academy")

lesson_text = st.text_area("Paste lesson content or textbook text here:", height=300)

if st.button("Generate Learning Aids"):
    if not lesson_text.strip():
        st.warning("Please provide some educational text to analyze.")
    else:
        with st.spinner("Generating..."):
            try:
                resp = requests.post(
                    "http://localhost:8000/generate/",
                    data={"text": lesson_text},
                    timeout=60
                )
                resp.raise_for_status()
                output = resp.json()

                st.subheader("🧠 Simplified Explanation")
                st.write(output.get("explanation"))

                st.subheader("📝 Quiz Questions & Answers")
                st.write(output.get("quiz"))

                st.subheader("🔑 Key Concepts")
                st.write(output.get("concepts"))

                # Download JSON
                st.download_button(
                    label="Download Learning Aids as JSON",
                    data=json.dumps(output, indent=2),
                    file_name="learning_aids.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Failed to generate learning aids: {e}")