import hashlib
import json
import logging
import time

import ollama
from agents.tools import run_tool
from config import MODEL
from storage.memory import get_history, save_message

logger = logging.getLogger('agents')

AGENT_RESPONSE_CACHE = {}
TOOL_RESULT_CACHE = {}
CACHE_MAX_SIZE = 100
TOOL_CACHE_MAX_SIZE = 200


def _make_cache_key(user_input: str, history_text: str) -> str:
    key_material = f"{user_input.strip()}||{history_text.strip()}"
    return hashlib.sha256(key_material.encode('utf-8')).hexdigest()


def _prune_cache(cache: dict, max_size: int):
    if len(cache) <= max_size:
        return
    while len(cache) > max_size:
        cache.pop(next(iter(cache)))


def _get_cached_tool_result(tool: str, tool_input: str):
    cache_key = (tool, tool_input)
    return TOOL_RESULT_CACHE.get(cache_key)


def _set_cached_tool_result(tool: str, tool_input: str, result):
    cache_key = (tool, tool_input)
    TOOL_RESULT_CACHE[cache_key] = result
    _prune_cache(TOOL_RESULT_CACHE, TOOL_CACHE_MAX_SIZE)


def _get_cached_agent_response(cache_key: str):
    return AGENT_RESPONSE_CACHE.get(cache_key)


def _set_cached_agent_response(cache_key: str, response: dict):
    AGENT_RESPONSE_CACHE[cache_key] = response
    _prune_cache(AGENT_RESPONSE_CACHE, CACHE_MAX_SIZE)


def _extract_json_from_text(text: str) -> dict:
    """Extract JSON object from text that may contain preamble/epilogue.
    
    Handles LLM responses like:
    'Here is JSON:\n{\n  "action": "chat"\n}\nHope this helps!'
    """
    # Find first { and last }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        raise json.JSONDecodeError("No JSON object found in response", text, 0)
    
    json_str = text[start_idx:end_idx + 1]
    return json.loads(json_str)


def agent_loop(user_input: str, max_steps=3):
    """Run the AI agent loop with tool calling capabilities."""
    logger.info(f"Agent loop started with input: {user_input[:100]}...",
                extra={'extra_fields': {'input_length': len(user_input), 'max_steps': max_steps}})

    start_time = time.time()
    context = user_input
    final_answer = None
    steps_taken = 0
    cache_key = None

    try:
        for step in range(max_steps):
            steps_taken = step + 1
            logger.debug(f"Agent step {step + 1}/{max_steps} started")

            # Fetch conversation history
            history = get_history()
            history_text = "\n".join(
                [f"{h['message']} -> {h['response']}" for h in history]
            ) if history else "No previous conversation"

            cache_key = _make_cache_key(user_input, history_text)
            cached_response = _get_cached_agent_response(cache_key)
            if cached_response:
                logger.info("Agent response served from cache",
                            extra={'extra_fields': {'cache_key': cache_key}})
                cached_response = cached_response.copy()
                cached_response['cached'] = True
                return cached_response

            # Build context with history
            context = f"""
Previous memory:
{history_text}

Current question:
{user_input}
"""

            prompt = f"""
You are an AI agent.

Available tools:
- sql
- explain_code
- chat

Conversation:
{context}

Respond ONLY in JSON format:

If using tool:
{{
  "action": "tool",
  "tool_name": "sql",
  "input": "your input"
}}

If final answer:
{{
  "action": "final",
  "answer": "your answer"
}}
"""

            step_start_time = time.time()

            try:
                response = ollama.chat(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )

                step_process_time = time.time() - step_start_time
                output = response["message"]["content"]

                logger.debug(f"LLM response received in {step_process_time:.2f}s",
                           extra={'extra_fields': {'step': step + 1, 'response_length': len(output)}})

            except Exception as e:
                logger.error(f"LLM call failed at step {step + 1}: {str(e)}", exc_info=True)
                return {"error": f"LLM communication failed: {str(e)}", "steps_taken": step}

            # 🧠 Parse LLM response as JSON
            try:
                data = _extract_json_from_text(output)

                if data["action"] == "final":
                    final_answer = data["answer"]
                    logger.info(f"Agent reached final answer at step {step + 1}",
                              extra={'extra_fields': {'step': step + 1, 'answer_length': len(final_answer)}})
                    break

                elif data["action"] == "tool":
                    tool = data["tool_name"]
                    tool_input = data["input"]

                    logger.info(f"Agent calling tool at step {step + 1}: {tool}",
                              extra={'extra_fields': {'step': step + 1, 'tool': tool, 'input_length': len(tool_input)}})

                    tool_start_time = time.time()
                    cached_tool_result = _get_cached_tool_result(tool, tool_input)
                    if cached_tool_result is not None:
                        tool_result = cached_tool_result
                        logger.info(f"Tool result served from cache for {tool}",
                                    extra={'extra_fields': {'tool': tool, 'step': step + 1}})
                    else:
                        tool_result = run_tool(tool, tool_input)
                        _set_cached_tool_result(tool, tool_input, tool_result)

                    tool_process_time = time.time() - tool_start_time
                    logger.info(f"Tool {tool} completed in {tool_process_time:.2f}s",
                              extra={'extra_fields': {'tool': tool, 'process_time': f"{tool_process_time:.2f}s"}})

                    # Add to context
                    context += f"\nTool: {tool}\nResult: {tool_result}\n"

                else:
                    logger.warning(f"Unknown action '{data.get('action')}' at step {step + 1}, continuing",
                                 extra={'extra_fields': {'step': step + 1, 'action': data.get('action')}})

            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing failed at step {step + 1}: {str(e)}",
                           extra={'extra_fields': {'step': step + 1, 'raw_output': output[:200]}},
                           exc_info=True)
                return {"error": f"JSON parsing failed: {str(e)}", "steps_taken": step + 1, "raw_output": output}
            except Exception as e:
                logger.error(f"Response parsing failed at step {step + 1}: {str(e)}",
                           extra={'extra_fields': {'step': step + 1, 'raw_output': output[:200]}},
                           exc_info=True)
                return {"error": f"Response parsing failed: {str(e)}", "steps_taken": step + 1, "raw_output": output}

        total_time = time.time() - start_time

        if final_answer:
            logger.info(f"Agent loop completed successfully in {total_time:.2f}s with {steps_taken} steps",
                      extra={'extra_fields': {'total_time': f"{total_time:.2f}s", 'steps_taken': steps_taken}})
            response = {
                "final_answer": final_answer,
                "steps_context": context,
                "steps_taken": steps_taken,
                "total_time": f"{total_time:.2f}s"
            }
            if cache_key:
                _set_cached_agent_response(cache_key, response)
            save_message("agent", user_input, final_answer)
            return response
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