import streamlit as st
import pandas as pd
import requests
import json

st.title("🏥 Medical Note Structurer")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload clinical notes CSV", type="csv")

if uploaded_file:
    # Read the uploaded CSV
    df = pd.read_csv(uploaded_file)
    results = []

    with st.spinner("Extracting info from notes..."):
        for _, row in df.iterrows():
            # Send note to backend API
            try:
                response = requests.post(
                    "http://localhost:8000/extract/",
                    data={"note": row["doctor_notes"]}
                )
                response.raise_for_status()  # Raise an error for bad status codes
                extracted = response.json()["structured"]

                # Parse the extracted JSON
                try:
                    structured = json.loads(extracted)
                except json.JSONDecodeError:
                    structured = {
                        "symptoms": "N/A",
                        "diagnosis": "N/A",
                        "medications": "N/A",
                        "follow_up": "N/A"
                    }

                # Append results with patient_id and structured data
                results.append({
                    "patient_id": row["patient_id"],
                    **structured
                })
            except requests.RequestException as e:
                # Handle API request errors
                st.error(f"Error processing note for patient {row['patient_id']}: {e}")
                results.append({
                    "patient_id": row["patient_id"],
                    "symptoms": "Error",
                    "diagnosis": "Error",
                    "medications": "Error",
                    "follow_up": "Error"
                })

        # Create result DataFrame
        result_df = pd.DataFrame(results)
        st.success("Extraction complete!")
        st.dataframe(result_df)

        # Download button for CSV
        st.download_button(
            label="Download Structured Notes",
            data=result_df.to_csv(index=False),
            file_name="structured_notes.csv",
            mime="text/csv"
        )