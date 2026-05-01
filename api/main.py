from fastapi import FastAPI
from llm.llm import ask_llm, explain_code
from storage.memory import save_message, get_history, delete_history
from agents.sql_agent import ask_database
from agents.agent import run_agent

app = FastAPI()

@app.get("/agent")
def agent(query: str):
    return run_agent(query)

@app.get("/ask")
def ask(question: str):
    response = ask_llm(question)
    save_message("user", question, response)
    return {"question": question, "response": response}

@app.get("/explain")
def explain(code: str):
    explanation = explain_code(code)
    return {"code": code, "explanation": explanation}


@app.get("/history")
def history(limit: int = 20):
    return get_history(limit)


@app.delete("/history")
def clear_history():
    deleted = delete_history()
    return {"deleted": deleted, "status": "ok"}

@app.get("/sql")
def sql(question: str):
    return ask_database(question)
