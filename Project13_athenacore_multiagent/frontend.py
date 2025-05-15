import streamlit as st
from orchestrator import run_agent
from tinydb import TinyDB, Query

# Initialize database
db = TinyDB("memory/memory_store.json")
Topic = Query()

# Streamlit app
st.title("🧠 AthenaCore: Multi-Agent Collaboration with Memory")

# Get existing topics
topics = [t["name"] for t in db.all()]

# Topic selection or creation
topic_option = st.selectbox("Choose or start a topic", options=topics + ["New Topic"])
if topic_option == "New Topic":
    topic = st.text_input("Enter new topic name")
else:
    topic = topic_option

# Agent selection
agent_choice = st.selectbox("Run agent", ["Research", "Summarizer", "Devil", "Insight"])

# Query input for Research Agent
query = st.text_area("Enter query or context (only for Research Agent):", "", disabled=agent_choice != "Research")

# Run agent button
if st.button("Run Agent") and topic:
    if topic_option == "New Topic" and not topic:
        st.error("Please enter a valid topic name.")
    else:
        result = run_agent(agent_choice, topic, query)
        st.subheader(f"{agent_choice} Agent Output")
        st.write(result)

# Display shared topic log
st.subheader("📜 Shared Topic Log")
if topic:
    result = db.search(Topic.name == topic)
    if result:
        for entry in result[0]["log"][::-1]:
            st.markdown(f"**{entry['agent']}**: {entry['content']}")
    else:
        st.write("No log entries for this topic yet.")