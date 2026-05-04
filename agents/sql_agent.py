from database.sql_db import get_connection
import ollama
import logging
import time

logger = logging.getLogger('agents.sql_agent')

def run_sql(query: str):
    """Execute SQL query and return results."""
    logger.info(f"Executing SQL query: {query[:100]}...",
                extra={'extra_fields': {'query_length': len(query)}})

    start_time = time.time()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        process_time = time.time() - start_time

        logger.info(f"SQL query executed successfully in {process_time:.2f}s: {len(result)} rows returned",
                   extra={'extra_fields': {
                       'process_time': f"{process_time:.2f}s",
                       'rows_returned': len(result)
                   }})

        return result

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"SQL query failed after {process_time:.2f}s: {str(e)}",
                    extra={'extra_fields': {
                        'process_time': f"{process_time:.2f}s",
                        'query': query[:200]
                    }},
                    exc_info=True)
        raise

def text_to_sql(question: str):
    """Convert natural language question to SQL using LLM."""
    logger.info(f"Converting question to SQL: {question[:100]}...",
                extra={'extra_fields': {'question_length': len(question)}})

    start_time = time.time()

    try:
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

        process_time = time.time() - start_time

        logger.info(f"SQL generation completed in {process_time:.2f}s",
                   extra={'extra_fields': {
                       'process_time': f"{process_time:.2f}s",
                       'sql_length': len(sql)
                   }})

        return sql

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"SQL generation failed after {process_time:.2f}s: {str(e)}",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s"}},
                    exc_info=True)
        raise

def ask_database(question: str):
    """Convert question to SQL and execute it."""
    logger.info(f"Database query request: {question[:100]}...",
                extra={'extra_fields': {'question_length': len(question)}})

    start_time = time.time()

    try:
        # Generate SQL from question
        sql = text_to_sql(question)

        if not is_safe_query(sql):
            return {"error": "Unsafe query blocked", "sql": sql}

        # Execute SQL
        result = run_sql(sql)

        total_time = time.time() - start_time

        logger.info(f"Database query completed in {total_time:.2f}s",
                   extra={'extra_fields': {
                       'total_time': f"{total_time:.2f}s",
                       'sql_query': sql[:200],
                       'result_rows': len(result)
                   }})

        return {
            "sql": sql,
            "result": result
        }

    except Exception as e:
        total_time = time.time() - start_time
        logger.error(f"Database query failed after {total_time:.2f}s: {str(e)}",
                    extra={'extra_fields': {'total_time': f"{total_time:.2f}s"}},
                    exc_info=True)
        raise

def is_safe_query(query: str):
    """Check if SQL query is safe (read-only)."""
    logger.info(f"Checking query safety: {query[:100]}...",
                extra={'extra_fields': {'query_length': len(query)}})

    forbidden = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER"]

    for word in forbidden:
        if word in query.upper():
            logger.warning(f"Unsafe query detected: contains '{word}'",
                         extra={'extra_fields': {
                             'forbidden_word': word,
                             'query': query[:200]
                         }})
            return False

    logger.info("Query passed safety check",
               extra={'extra_fields': {'query_length': len(query)}})
    return True