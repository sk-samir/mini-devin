from database.sql_db import get_connection
import ollama

def run_sql(query: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def text_to_sql(question: str):
    prompt = f"""
Convert this question into SQL for MySQL:

Question: {question}

Database table:
users(id, name, city)

Return only the SQL query, nothing else.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response["message"]["content"].strip()
    # Extract SQL if wrapped in code blocks
    if "```sql" in sql:
        sql = sql.split("```sql")[1].split("```")[0].strip()
    elif "```" in sql:
        sql = sql.split("```")[1].split("```")[0].strip()
    return sql

def ask_database(question: str):
    sql = text_to_sql(question)

    result = run_sql(sql)

    return {
        "sql": sql,
        "result": result
    }
