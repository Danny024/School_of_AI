import streamlit as st
import pandas as pd
import requests
import json

st.title("🏥 Medical Note Structurer")

# Upload a CSV of clinical notes with at least 'patient_id' and 'note' columns
uploaded_file = st.file_uploader("Upload clinical notes CSV", type="csv")
if uploaded_file:
    # Read the uploaded CSV into a DataFrame
    df = pd.read_csv(uploaded_file)
    results = []

    # Process each note
    with st.spinner("Extracting info from notes..."):
        for _, row in df.iterrows():
            # Extract the note text (adjust column name if needed)
            note_text = row.get("note", "")
            try:
                # Send to your extraction service
                response = requests.post(
                    "http://localhost:8000/extract/",
                    json={"note": note_text},
                    timeout=30
                )
                response.raise_for_status()
                extracted = response.json().get("structured", "{}")
                structured = json.loads(extracted)
            except (requests.RequestException, json.JSONDecodeError, KeyError):
                # Fallback in case of errors
                structured = {"symptoms": "N/A", "diagnosis": "N/A", "medication": "N/A"}

            # Build a result record
            results.append({
                "patient_id": row.get("patient_id", ""),
                "symptoms": structured.get("symptoms", "N/A"),
                "diagnosis": structured.get("diagnosis", "N/A"),
                "medication": structured.get("medication", "N/A"),
            })

    # Convert to DataFrame and display
    result_df = pd.DataFrame(results)
    st.success("Extraction complete!")
    st.dataframe(result_df)

    # Provide download button for the structured results
    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Structured Notes",
        data=csv,
        file_name="structured_notes.csv",
        mime="text/csv"
    )
