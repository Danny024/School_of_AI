# import streamlit as st
# import pandas as pd
# import requests

# st.title("🛒 Acme Product Review Analyzer")
# uploaded_file = st.file_uploader("Upload CSV file with product reviews", type=["csv"])

# if uploaded_file:
#     # Read the uploaded CSV file
#     df = pd.read_csv(uploaded_file)
#     results = []

#     with st.spinner("Analyzing reviews..."):
#         for _, row in df.iterrows():
#             review_text = row["review_text"]
#             try:
#                 # Send POST request to FastAPI endpoint
#                 res = requests.post(
#                     "http://localhost:8000/analyze/",
#                     data={"text": review_text},
#                     timeout=10
#                 )
#                 res.raise_for_status()  # Raise exception for bad status codes
#                 data = res.json()
#                 results.append({
#                     "product_name": row["product_name"],
#                     "review_text": review_text,
#                     **data  # Unpack sentiment, topic, summary
#                 })
#             except requests.RequestException as e:
#                 st.warning(f"Error analyzing review for {row['product_name']}: {str(e)}")
    
#     result_df = pd.DataFrame(results)
#     st.success("Analysis complete!")

#     st.dataframe(result_df)
#     st.download_button(
#         label="Download Results as CSV",
#         data=result_df.to_csv(index=False)
#     )
#     st.subheader("📊 Sentiment Distribution")
#     st.bar_chart(result_df["sentiment"].value_counts())
#     st.subheader("📌 Top Topics")
#     st.bar_chart(result_df["topic"].value_counts())


import streamlit as st
import pandas as pd
import requests

# Set page title
st.title("🛒 Acme Product Review Analyzer")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload CSV file with product reviews", type=["csv"])

if uploaded_file:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Ensure required columns exist
    if "review_text" not in df.columns or "product_name" not in df.columns:
        st.error("CSV must contain 'review_text' and 'product_name' columns.")
    else:
        results = []
        with st.spinner("Analyzing reviews..."):
            for _, row in df.iterrows():
                review_text = row["review_text"]
                try:
                    # Send POST request to FastAPI endpoint
                    res = requests.post(
                        "http://localhost:8000/analyze/",
                        data={"text": review_text},
                        timeout=10
                    )
                    res.raise_for_status()  # Raise exception for bad status codes
                    data = res.json()
                    
                    # Debug: Display the response to verify structure
                    st.write(f"API response for {row['product_name']}: {data}")
                    
                    # Check if expected keys are in the response
                    if "sentiment" not in data or "topic" not in data or "summary" not in data:
                        st.warning(f"Unexpected response format for {row['product_name']}: {data}")
                        continue
                    
                    results.append({
                        "product_name": row["product_name"],
                        "review_text": review_text,
                        "sentiment": data["sentiment"],
                        "topic": data["topic"],
                        "summary": data["summary"]
                    })
                except requests.RequestException as e:
                    st.warning(f"Error analyzing review for {row['product_name']}: {str(e)}")
        
        # Check if results are empty
        if not results:
            st.error("No valid analysis results were obtained. Check the FastAPI endpoint.")
        else:
            # Create DataFrame from results
            result_df = pd.DataFrame(results)
            
            # Display success message and results
            st.success("Analysis complete!")
            st.dataframe(result_df)
            
            # Download button for results
            st.download_button(
                label="Download Results as CSV",
                data=result_df.to_csv(index=False),
                file_name="analyzed_reviews.csv",
                mime="text/csv"
            )
            
            # Sentiment distribution chart
            st.subheader("📊 Sentiment Distribution")
            if "sentiment" in result_df.columns and not result_df["sentiment"].empty:
                st.bar_chart(result_df["sentiment"].value_counts())
            else:
                st.write("No sentiment data to display. Check API response.")
            
            # Top topics chart
            st.subheader("📌 Top Topics")
            if "topic" in result_df.columns and not result_df["topic"].empty:
                st.bar_chart(result_df["topic"].value_counts())
            else:
                st.write("No topic data to display. Check API response.")