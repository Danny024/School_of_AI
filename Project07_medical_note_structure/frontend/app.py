import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Medical Note Structurer", layout="wide")
st.title("🏥 Medical Note Structurer")

# Check backend health
try:
    health_response = requests.get("http://localhost:8000/health", timeout=5)
    health_response.raise_for_status()
    st.success(f"Backend is healthy: {health_response.json()}")
except requests.RequestException as e:
    st.error(f"Backend health check failed: {e}")

uploaded_file = st.file_uploader("Upload clinical notes CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    required_cols = {"patient_id", "note"}
    if not required_cols.issubset(df.columns):
        st.error(f"CSV must contain columns: {required_cols}")
    else:
        results = []
        with st.spinner("Extracting info from notes..."):
            for _, row in df.iterrows():
                pid = str(row["patient_id"])
                note = row["note"]
                try:
                    response = requests.post(
                        "http://localhost:8000/extract/",
                        data={"patient_id": pid, "note": note},
                        timeout=30
                    )
                    response.raise_for_status()
                    out = response.json()
                    structured = out["structured"]
                    structured["summary"] = out.get("summary", "")
                except requests.RequestException as e:
                    error_detail = str(e)
                    if 'response' in locals():
                        try:
                            error_detail = response.json().get("detail", str(e))
                        except:
                            pass
                    st.error(f"Error processing note for patient {pid}: {error_detail}")
                    structured = {
                        "patient_id": pid,
                        "symptoms": "N/A",
                        "diagnosis": "N/A",
                        "medications": "N/A",
                        "follow_up": "N/A",
                        "summary": ""
                    }
                results.append(structured)

        result_df = pd.DataFrame(results)
        st.success("Extraction complete!")
        st.dataframe(result_df)

        csv_data = result_df.to_csv(index=False)
        st.download_button(
            "Download Structured Notes",
            csv_data,
            file_name="structured_notes.csv",
            mime="text/csv"
        )