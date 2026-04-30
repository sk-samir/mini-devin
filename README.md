# Mini Devin Project
Your agent will:
Understand a user request
Plan steps
Generate code / SQL
Execute it
Detect errors
Fix errors automatically
Return results
 ## Prerequisites
 Python 3.12+ ,MongoDB installed and running locally
 A workspace virtual environment in .venv
 ## Setup\
 1. Activate the virtual environment:\r\n   \.venv\Scripts\activate\r\n
 2. Install dependencies:\r\n   pip install -r requirements.txt\r\n\r\n## Start MongoDB\r\nMake sure MongoDB is running locally on mongodb://localhost:27017/.\r\nIf you need to start MongoDB manually, use:\r\n   mongod --dbpath C:\\data\\db\r\n\r\n## Run the backend\r\nFrom the project root, start FastAPI with Uvicorn:\r\n   \.venv\Scripts\python.exe -m uvicorn app.main:app --reload\r\n\r\n## Run the frontend\r\nFrom the project root, start Streamlit:\r\n   \.venv\Scripts\python.exe -m streamlit run ui.py\r\n\r\n## What it does\r\n- The Streamlit UI submits questions to the backend at http://127.0.0.1:8000/ask.\r\n- The backend sends prompts to the Ollama model and stores conversation records in MongoDB.\r\n- The UI also loads existing saved chat history from http://127.0.0.1:8000/history.\r\n\r\n## Notes\r\n- If you change backend code, restart the Uvicorn server or use --reload to auto-reload.\r\n- Chat history is saved in MongoDB collection mini_devin.chat_memory.\r\n- If history fails to load, verify that the backend is running and that /history returns status 200.\r\n
