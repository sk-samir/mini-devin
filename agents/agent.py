import ollama
from agents.tools import run_tool
import logging
import time

logger = logging.getLogger('agents')

def agent_loop(user_input: str, max_steps=3):
    """Run the AI agent loop with tool calling capabilities."""
    logger.info(f"Agent loop started with input: {user_input[:100]}...",
                extra={'extra_fields': {'input_length': len(user_input), 'max_steps': max_steps}})

    start_time = time.time()
    context = user_input
    final_answer = None
    steps_taken = 0

    try:
        for step in range(max_steps):
            steps_taken = step + 1
            logger.debug(f"Agent step {step + 1}/{max_steps} started")

            prompt = f"""
You are an AI agent.

You can:
- use tools: sql, explain_code, chat
- or return FINAL answer

Conversation so far:
{context}

Decide next step.

Format:
TOOL: <tool_name>
INPUT: <input>

OR

FINAL: <your final answer>
"""

            step_start_time = time.time()

            try:
                response = ollama.chat(
                    model="llama3",
                    messages=[{"role": "user", "content": prompt}]
                )

                step_process_time = time.time() - step_start_time
                output = response["message"]["content"]

                logger.debug(f"LLM response received in {step_process_time:.2f}s",
                           extra={'extra_fields': {'step': step + 1, 'response_length': len(output)}})

            except Exception as e:
                logger.error(f"LLM call failed at step {step + 1}: {str(e)}", exc_info=True)
                return {"error": f"LLM communication failed: {str(e)}", "steps_taken": step}

            # 🧠 Check if final answer
            if "FINAL:" in output:
                final_answer = output.split("FINAL:")[1].strip()
                logger.info(f"Agent reached final answer at step {step + 1}",
                          extra={'extra_fields': {'step': step + 1, 'answer_length': len(final_answer)}})
                break

            # 🛠️ Parse tool call
            try:
                tool_lines = [line for line in output.split("\n") if "TOOL:" in line]
                input_lines = [line for line in output.split("\n") if "INPUT:" in line]

                if not tool_lines or not input_lines:
                    logger.warning(f"No valid tool call found at step {step + 1}, raw output: {output[:200]}...")
                    continue

                tool = tool_lines[0].split("TOOL:")[1].strip()
                tool_input = input_lines[0].split("INPUT:")[1].strip()

                logger.info(f"Agent calling tool at step {step + 1}: {tool}",
                          extra={'extra_fields': {'step': step + 1, 'tool': tool, 'input_length': len(tool_input)}})

                tool_start_time = time.time()
                tool_result = run_tool(tool, tool_input)
                tool_process_time = time.time() - tool_start_time

                logger.info(f"Tool {tool} completed in {tool_process_time:.2f}s",
                          extra={'extra_fields': {'tool': tool, 'process_time': f"{tool_process_time:.2f}s"}})

                # Add to context
                context += f"\nTool used: {tool}\nResult: {tool_result}\n"

            except Exception as e:
                logger.error(f"Tool call parsing/execution failed at step {step + 1}: {str(e)}",
                           extra={'extra_fields': {'step': step + 1, 'raw_output': output[:200]}},
                           exc_info=True)
                return {"error": f"Tool execution failed: {str(e)}", "steps_taken": step + 1, "raw_output": output}

        total_time = time.time() - start_time

        if final_answer:
            logger.info(f"Agent loop completed successfully in {total_time:.2f}s with {steps_taken} steps",
                      extra={'extra_fields': {'total_time': f"{total_time:.2f}s", 'steps_taken': steps_taken}})
            return {
                "final_answer": final_answer,
                "steps_context": context,
                "steps_taken": steps_taken,
                "total_time": f"{total_time:.2f}s"
            }
        else:
            logger.warning(f"Agent loop reached max steps ({max_steps}) without final answer",
                         extra={'extra_fields': {'total_time': f"{total_time:.2f}s", 'steps_taken': steps_taken}})
            return {
                "error": f"Reached maximum steps ({max_steps}) without final answer",
                "steps_context": context,
                "steps_taken": steps_taken,
                "total_time": f"{total_time:.2f}s"
            }

    except Exception as e:
        total_time = time.time() - start_time
        logger.error(f"Agent loop failed after {total_time:.2f}s: {str(e)}",
                   extra={'extra_fields': {'total_time': f"{total_time:.2f}s", 'steps_taken': steps_taken}},
                   exc_info=True)
        return {"error": f"Agent loop failed: {str(e)}", "steps_taken": steps_taken}