import streamlit as st
import pandas as pd
import requests
from collections import Counter

st.title("🛒 Acme Product Review Analyzer")


uploaded_file = st.file_uploader(
    "Upload CSV file with product reviews", 
    type="csv"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    results = []
    with st.spinner("Analyzing reviews..."):
        for _, row in df.iterrows():
            review_text = row["review_text"]
            res = requests.post(
                "http://localhost:8000/analyze/",
                json={"text": review_text},
                timeout=30
            )
            data = res.json()
            results.append({
                "product_name": row.get("product_name", ""),
                "review_text": review_text,
                **data
            })

    result_df = pd.DataFrame(results)
    st.success("Analysis complete!")
    st.dataframe(result_df)

    csv_bytes = result_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Results as CSV",
        data=csv_bytes,
        file_name="analysis_results.csv",
        mime="text/csv"
    )

    st.subheader("📊 Sentiment Distribution")
    if "sentiment" in result_df.columns:
        sentiment_counts = result_df["sentiment"].value_counts()
        st.bar_chart(sentiment_counts)
    else:
        st.write("No `sentiment` field in API response.")

    st.subheader("📌 Top Topics")
    if "topic" in result_df.columns:
        topic_counts = result_df["topic"].value_counts().nlargest(10)
        st.bar_chart(topic_counts)

    elif "topics" in result_df.columns:
        all_topics = Counter()
        for topics in result_df["topics"].dropna():
            if isinstance(topics, list):
                all_topics.update(topics)
            else:
                all_topics.update([topics])
        top_topics = pd.Series(dict(all_topics)).sort_values(ascending=False).head(10)
        st.bar_chart(top_topics)

    else:
        st.write("No `topic` or `topics` field in API response.")
