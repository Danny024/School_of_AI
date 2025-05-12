import streamlit as st
import requests
import json

# Page config
st.set_page_config(page_title="Earnings Call Analyzer", layout="wide")
st.title("📈 Earnings Call Analyzer")

# Input area
transcript = st.text_area("Paste earnings call transcript here:", height=300)

if st.button("Analyze"):  
    if not transcript.strip():
        st.warning("Please paste a transcript to analyze.")
    else:
        with st.spinner("Running analysis..."):
            try:
                resp = requests.post(
                    "http://localhost:8000/analyze/",
                    data={"text": transcript},
                    timeout=60
                )
                resp.raise_for_status()
                output = resp.json()

                st.subheader("📝 Summary")
                st.write(output.get("summary"))

                st.subheader("📊 Sentiment")
                st.write(output.get("sentiment"))

                st.subheader("💡 Key Insights")
                st.write(output.get("insights"))

                # Download JSON
                st.download_button(
                    label="Download Analysis as JSON",
                    data=json.dumps(output, indent=2),
                    file_name="earnings_analysis.json",
                    mime="application/json"
                )

            except Exception as e:
                st.error(f"Analysis failed: {e}")