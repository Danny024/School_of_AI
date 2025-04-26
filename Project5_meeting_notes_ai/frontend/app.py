import streamlit as st
import requests

st.title("🎙 Meeting Notes Generator")

audio_file = st.file_uploader("Upload your meetiing audio (.mp3 or .wav)", type=["mp3", "wav"] )

if audio_file:
    st.audio(audio_file)

    if st.button("Generate Notes"):
        with st.spinner("Processing audio ..."):
            res = requests.post("http://localhost:8000/process/", files={"file": audio_file.getvalue()})

            if res.status_code == 200:
                output = res.json()

                st.subheader("📝 Summary:")
                st.write(output["summary"])

                st.subheader("✅ Action Items:")
                st.write(output["action_items"])

                st.subheader("📄 Full Transcript:")
                with st.expander("Show Transcript"):
                    st.text_area("Transcript", value=output["transcript"], height=300)
            else:
                st.error("Failed to generate notes. Please try again.")