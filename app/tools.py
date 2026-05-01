from app.sql_agent import ask_database
from app.llm import ask_llm, explain_code

def run_tool(tool_name: str, input_text: str):
    if tool_name == "sql":
        return ask_database(input_text)

    elif tool_name == "explain_code":
        return explain_code(input_text)

    elif tool_name == "chat":
        return ask_llm(input_text)

    else:
        return "Unknown tool"