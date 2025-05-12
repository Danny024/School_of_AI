# import streamlit as st
# import requests
# st.title(" Legal Document Analyzer")
# text_input = st.text_area("Paste legal text here:", height=300)
# if st.button("Analyze"):
#     response = requests.post("http://localhost:8000/analyze/", data={"text": t
#     results = response.json()
#     st.subheader("📄 Summary")
#     st.write(results["summary"])
#     st.subheader("📌 Key Clauses")
#     st.write(results["clauses"])
#     st.subheader("🔍 Named Entities")
#     st.write(results["entities"])


import streamlit as st
import requests

st.set_page_config(page_title="LexPro Legal Analyzer", layout="wide")
st.title("📑 LexPro Legal Document Analyzer")

text = st.text_area("Paste or type legal text here:", height=300)
if st.button("Analyze Document"):
    if not text.strip():
        st.warning("Please provide some legal text to analyze.")
    else:
        with st.spinner("Analyzing..."):
            try:
                resp = requests.post(
                    "http://localhost:8000/analyze/", data={"text": text}, timeout=60
                )
                resp.raise_for_status()
                results = resp.json()

                st.subheader("📄 Case Summary")
                st.write(results.get("summary"))

                st.subheader("📌 Key Clauses")
                st.write(results.get("clauses"))

                st.subheader("🔍 Named Entities")
                st.write(results.get("entities"))

                # Offer download
                import json
                st.download_button(
                    "Download JSON", json.dumps(results, indent=2), "analysis.json", "application/json"
                )
            except Exception as e:
                st.error(f"Analysis failed: {e}")