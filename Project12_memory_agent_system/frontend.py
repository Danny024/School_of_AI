import streamlit as st
from orchestrator import handle_query
from tinydb import TinyDB, Query
import json
from agents import memory_agents
import pandas as pd

st.title("🧠 Persistent Memory Agent")

# Initialize TinyDB
db = TinyDB("memory/memory_store.json")
Topic = Query()

# Get existing topics
topics = [item["name"] for item in db.all()]

# Topic selection or creation
selected_topic = st.selectbox(
    "Choose or create a topic",
    options=["Start new topic"] + topics,
    index=0
)

if selected_topic == "Start new topic":
    new_topic = st.text_input("Enter new topic name")
    selected_topic = new_topic if new_topic else None

# User input
user_input = st.text_area("Ask a question or input research note:")

# Submit button
if st.button("Submit"):
    if not selected_topic:
        st.error("Please select or enter a valid topic.")
    elif not user_input:
        st.error("Please enter a question or note.")
    else:
        with st.spinner("Processing your query..."):
            try:
                response, history = handle_query(selected_topic, user_input)
                
                # Display AI response
                st.subheader("💬 AI Response")
                st.markdown(response)
                
                # Display topic memory log (most recent first)
                st.subheader("📜 Topic Memory Log")
                for entry in history[::-1]:
                    st.markdown(f"**You**: {entry['user']}")
                    st.markdown(f"**AI**: {entry['ai']}")
                    st.markdown("---")
                
                # Export session summary
                st.subheader("📥 Export Session Summary")
                summary_data = {
                    "topic": selected_topic,
                    "history": history
                }
                summary_json = json.dumps(summary_data, indent=2)
                st.download_button(
                    label="Download JSON Summary",
                    data=summary_json,
                    file_name=f"{selected_topic}_summary.json",
                    mime="application/json"
                )
                
                # Optional CSV export
                df = pd.DataFrame(history)
                st.download_button(
                    label="Download CSV Summary",
                    data=df.to_csv(index=False),
                    file_name=f"{selected_topic}_summary.csv",
                    mime="text/csv"
                )
                
            except Exception as e:
                st.error(f"Error processing query: {e}")

# Display all topics and their summaries
st.subheader("📋 All Topics")
if topics:
    for topic in topics:
        with st.expander(f"Topic: {topic}"):
            history = memory_agents.get_topic_history(topic)
            for entry in history[::-1]:
                st.markdown(f"**You**: {entry['user']}")
                st.markdown(f"**AI**: {entry['ai']}")
                st.markdown("---")
else:
    st.info("No topics created yet. Start a new topic above!")