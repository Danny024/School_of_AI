import streamlit as st
import requests
st.title("Sentiment Analyzer (Mistral)")

text_input = st.text_area("Enter your sentence here:")

if st.button("Analyze"):
    res = requests.post("http://localhost:8000/analyze/", data={"text": text_input})
    sentiment = res.json().get("sentiment", "Error")
    st.subheader("Predicted Sentiment:")
    st.write(sentiment)