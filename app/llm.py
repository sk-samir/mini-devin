import ollama

def ask_llm(prompt: str) -> str:
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]

def explain_code(code: str) -> str:
    prompt = f"Explain this code clearly:\n{code}"
    
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"]