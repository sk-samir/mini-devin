from fastapi import FastAPI
from app.llm import ask_llm
from app.llm import explain_code
from memory import save_message, get_history

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Mini Devin is running 🚀"}

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

 