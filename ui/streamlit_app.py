import streamlit as st
import requests
import logging
import time

# Initialize logging for UI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ui')

st.title("🚀 Mini Devin Chat")

logger.info("Mini Devin UI started")

if "chat" not in st.session_state:
    st.session_state.chat = []
    logger.debug("Initialized chat session state")

history = []
try:
    logger.debug("Attempting to load chat history")
    start_time = time.time()
    history = requests.get("http://127.0.0.1:8000/history", params={"limit": 20}).json()
    load_time = time.time() - start_time
    logger.info(f"Chat history loaded successfully in {load_time:.2f}s: {len(history)} records")
except Exception as e:
    logger.error(f"Failed to load chat history: {str(e)}")
    st.error("Unable to load saved chat history from the backend.")

if st.button("Clear saved chat history"):
    try:
        logger.info("User requested to clear chat history")
        start_time = time.time()
        result = requests.delete("http://127.0.0.1:8000/history")
        if result.status_code == 200:
            clear_time = time.time() - start_time
            logger.info(f"Chat history cleared successfully in {clear_time:.2f}s")
            st.success("Saved chat history cleared.")
            history = []
        else:
            logger.error(f"Failed to clear history: HTTP {result.status_code}")
            st.error("Failed to clear history.")
    except Exception as e:
        logger.error(f"Failed to contact backend for history clear: {str(e)}")
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
    logger.info(f"User submitted question: {user_input[:100]}...")
    start_time = time.time()

    try:
        # call FastAPI backend
        response = requests.get(
            "http://127.0.0.1:8000/ask",
            params={"question": user_input}
        ).json()

        process_time = time.time() - start_time
        logger.info(f"Backend response received in {process_time:.2f}s")

        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("AI", response["response"]))

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Failed to get response from backend after {process_time:.2f}s: {str(e)}")
        st.error(f"Failed to get response: {str(e)}")

for role, msg in st.session_state.chat:
    st.write(f"**{role}:** {msg}")

# Add a simple health check
try:
    health_response = requests.get("http://127.0.0.1:8000/health", timeout=5)
    if health_response.status_code == 200:
        st.sidebar.success("✅ Backend Connected")
    else:
        st.sidebar.error("❌ Backend Issues")
except:
    st.sidebar.warning("⚠️ Backend Unreachable")
