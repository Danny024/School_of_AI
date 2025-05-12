import streamlit as st
from orchestrator import run_research_pipeline

st.title("🧠 Multi-Agent Research Assistant")

topic = st.text_input("Enter a research topic (e.g., 'AI trends in healthcare')")

if st.button("Run Research"):
    if not topic:
        st.error("Please enter a research topic.")
    else:
        with st.spinner("Running research pipeline..."):
            try:
                result = run_research_pipeline(topic)
                
                st.subheader("🔍 Search Results")
                st.text(result["search"])
                
                st.subheader("📝 Summary")
                st.text(result["summary"])
                
                st.subheader("✅ Fact-Checker Feedback")
                st.text(result["corrections"])
                
                st.subheader("📄 Final Report")
                st.markdown(result["report"])
                
            except Exception as e:
                st.error(f"Error running research pipeline: {e}")