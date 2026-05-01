from agents.sql_agent import ask_database
from agents.tools import run_tool

def choose_tool(user_input: str):
    prompt = f"""
You are an AI agent. Decide which tool to use.

Tools:
1. sql → for database queries
2. explain_code → for code explanation
3. chat → general questions

User input: {user_input}

Return ONLY one word: sql OR explain_code OR chat
"""

    import ollama
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()


def run_agent(user_input: str):
    tool = choose_tool(user_input)

    result = run_tool(tool, user_input)

    return {
        "tool_used": tool,
        "result": result
    }
