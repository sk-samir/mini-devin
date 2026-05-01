# Quick Start Guide

## Prerequisites Check

Run this to verify everything is set up correctly:

```bash
python verify_structure.py
```

Expected output should show ✅ all checks passing.

## Setup Steps

### 1. Activate Virtual Environment

#### Windows (Command Prompt):
```cmd
.\.venv\Scripts\activate.bat
```

#### Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

#### macOS/Linux:
```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Services

#### Option A: Using Python Scripts

**Terminal 1 - Start Backend:**
```bash
python run_backend.py
```

**Terminal 2 - Start Frontend:**
```bash
python run_frontend.py
```

#### Option B: Using Batch Files (Windows)

**Terminal 1:**
```cmd
start_backend.bat
```

**Terminal 2:**
```cmd
start_frontend.bat
```

#### Option C: Using PowerShell Scripts (Windows)

**Terminal 1:**
```powershell
.\start_backend.ps1
```

**Terminal 2:**
```powershell
.\start_frontend.ps1
```

#### Option D: Direct Commands

**Terminal 1 - Backend:**
```bash
python -m uvicorn api.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
python -m streamlit run ui/streamlit_app.py
```

## Access the Application

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend (FastAPI)**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## Project Structure

```
mini-devin/
├── llm/                   # LLM interactions
│   ├── llm.py            # ask_llm(), explain_code()
├── agents/                # Agent logic
│   ├── agent.py          # Main agent
│   ├── sql_agent.py      # SQL queries
│   └── tools.py          # Tool runner
├── database/              # Database layer
│   └── sql_db.py         # MySQL connection
├── storage/               # Persistence layer
│   └── memory.py         # MongoDB history
├── api/                   # FastAPI backend
│   └── main.py           # API endpoints
├── ui/                    # Streamlit UI
│   └── streamlit_app.py  # Frontend
├── requirements.txt       # Dependencies
├── run_backend.py         # Backend entry point
├── run_frontend.py        # Frontend entry point
└── README.md             # Full documentation
```

## Services Required

Before running, ensure these services are running:

1. **MongoDB**: `mongod --dbpath C:\data\db`
2. **MySQL**: Your MySQL server with `mini_devin` database
3. **Ollama**: With `llama3` model available

## Troubleshooting

### Backend won't start
- Check if MongoDB is running
- Verify MySQL is running and credentials are correct in `database/sql_db.py`
- Ensure Ollama is running with `llama3` model

### Frontend can't connect to backend
- Verify backend is running on `http://127.0.0.1:8000`
- Check firewall settings
- Try accessing `http://127.0.0.1:8000/docs` in browser to confirm backend is up

### ImportError when running
- Run `python verify_structure.py` to check project structure
- Ensure virtual environment is activated
- Try `pip install -r requirements.txt` again

## Quick Test

Once both services are running, test the API:

```bash
curl "http://127.0.0.1:8000/ask?question=What%20is%202%2B2%3F"
```

Expected response:
```json
{
  "question": "What is 2+2?",
  "response": "LLM response here..."
}
```

## API Endpoints

- `GET /agent?query=<query>` - Run agent
- `GET /ask?question=<question>` - Ask LLM
- `GET /explain?code=<code>` - Explain code
- `GET /sql?question=<question>` - Query database
- `GET /history?limit=20` - Get chat history
- `DELETE /history` - Clear history

## Need Help?

Check [README.md](README.md) for detailed documentation.
