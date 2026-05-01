import streamlit as st
import requests

st.title("🚀 Mini Devin Chat")

if "chat" not in st.session_state:
    st.session_state.chat = []

history = []
try:
    history = requests.get("http://127.0.0.1:8000/history", params={"limit": 20}).json()
except Exception:
    st.error("Unable to load saved chat history from the backend.")

if st.button("Clear saved chat history"):
    try:
        result = requests.delete("http://127.0.0.1:8000/history")
        if result.status_code == 200:
            st.success("Saved chat history cleared.")
            history = []
        else:
            st.error("Failed to clear history.")
    except Exception:
        st.error("Unable to contact backend to clear history.")

if history:
    st.subheader("Saved Chat History")
    for entry in history:
        st.markdown(f"**{entry['user'].capitalize()}:** {entry['message']}")
        st.markdown(f"**AI:** {entry['response']}")
        if entry.get("created_at"):
            st.caption(entry["created_at"])
        st.markdown("---")

user_input = st.text_input("Ask me anything:")

if user_input:
    # call FastAPI backend
    response = requests.get(
        "http://127.0.0.1:8000/ask",
        params={"question": user_input}
    ).json()

    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("AI", response["response"]))

for role, msg in st.session_state.chat:
    st.write(f"**{role}:** {msg}")
