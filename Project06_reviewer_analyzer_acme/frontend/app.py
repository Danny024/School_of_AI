import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Acme Review Analyzer", layout="wide")
st.title("🛒 Acme Product Review Analyzer")

uploaded_file = st.file_uploader(
    "Upload CSV file with product reviews", type="csv"
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "review_text" not in df.columns or "product_name" not in df.columns:
        st.error("CSV must contain 'product_name' and 'review_text' columns.")
    else:
        results = []
        with st.spinner("Analyzing reviews..."):
            for _, row in df.iterrows():
                text = row["review_text"]
                try:
                    res = requests.post(
                        "http://localhost:8000/analyze/",
                        data={"text": text},
                        timeout=30,
                    )
                    res.raise_for_status()
                    analysis = res.json()
                except Exception as e:
                    st.error(f"Error analyzing review: {e}")
                    analysis = {"sentiment": "Error", "topic": "Error", "summary": "Error"}

                results.append({
                    "product_name": row["product_name"],
                    "review_text": text,
                    **analysis,
                })

        result_df = pd.DataFrame(results)

        st.subheader("✅ Analysis Complete")
        st.dataframe(result_df)
        st.download_button(
            "Download Results as CSV",
            data=result_df.to_csv(index=False),
            file_name="analyzed_reviews.csv",
            mime="text/csv",
        )

        st.subheader("📊 Sentiment Distribution")
        st.bar_chart(result_df["sentiment"].value_counts())

        st.subheader("📌 Top Topics")
        st.bar_chart(result_df["topic"].value_counts())