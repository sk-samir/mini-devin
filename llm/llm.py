import ollama
import logging
import time

logger = logging.getLogger('llm')

def ask_llm(prompt: str) -> str:
    """Ask the LLM a question and return the response."""
    logger.info(f"LLM question received: {prompt[:100]}...",
                extra={'extra_fields': {'prompt_length': len(prompt)}})

    start_time = time.time()

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response["message"]["content"]
        process_time = time.time() - start_time

        logger.info(f"LLM question answered in {process_time:.2f}s",
                   extra={'extra_fields': {
                       'process_time': f"{process_time:.2f}s",
                       'response_length': len(answer)
                   }})

        return answer

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"LLM question failed after {process_time:.2f}s: {str(e)}",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s"}},
                    exc_info=True)
        raise

def explain_code(code: str) -> str:
    """Explain the provided code using LLM."""
    logger.info(f"Code explanation requested: {len(code)} characters",
                extra={'extra_fields': {'code_length': len(code)}})

    start_time = time.time()

    try:
        prompt = f"Explain this code clearly:\n{code}"

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        explanation = response["message"]["content"]
        process_time = time.time() - start_time

        logger.info(f"Code explanation completed in {process_time:.2f}s",
                   extra={'extra_fields': {
                       'process_time': f"{process_time:.2f}s",
                       'explanation_length': len(explanation)
                   }})

        return explanation

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Code explanation failed after {process_time:.2f}s: {str(e)}",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s"}},
                    exc_info=True)
        raise
