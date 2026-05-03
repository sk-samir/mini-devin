from agents.sql_agent import ask_database
from llm.llm import ask_llm, explain_code
import logging
import time

logger = logging.getLogger('agents.tools')

def run_tool(tool_name: str, input_text: str):
    """Execute the specified tool with the given input."""
    logger.info(f"Tool execution requested: {tool_name}",
                extra={'extra_fields': {'tool': tool_name, 'input_length': len(input_text)}})

    start_time = time.time()

    try:
        if tool_name == "sql":
            logger.debug("Executing SQL tool")
            result = ask_database(input_text)

        elif tool_name == "explain_code":
            logger.debug("Executing code explanation tool")
            result = explain_code(input_text)

        elif tool_name == "chat":
            logger.debug("Executing chat tool")
            result = ask_llm(input_text)

        else:
            logger.warning(f"Unknown tool requested: {tool_name}")
            result = f"Unknown tool: {tool_name}"

        process_time = time.time() - start_time

        logger.info(f"Tool {tool_name} completed successfully in {process_time:.2f}s",
                   extra={'extra_fields': {
                       'tool': tool_name,
                       'process_time': f"{process_time:.2f}s",
                       'result_type': type(result).__name__
                   }})

        return result

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Tool {tool_name} failed after {process_time:.2f}s: {str(e)}",
                    extra={'extra_fields': {
                        'tool': tool_name,
                        'process_time': f"{process_time:.2f}s"
                    }},
                    exc_info=True)
        return f"Tool execution failed: {str(e)}"
