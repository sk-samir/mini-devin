#!/usr/bin/env python
"""Test JSON extraction fix for agent."""

import json
from agents.agent import _extract_json_from_text

def test_json_extraction():
    """Test cases for JSON extraction with preamble/epilogue."""
    
    # Test case 1: with preamble and epilogue (from the error)
    test1 = """Here is the response in JSON format:

{
  "action": "chat",
  "message": "Hello! It's nice to meet you. Is there something I can help you with, or would you like to chat?"
}

Please let me know how I can assist you further."""
    
    result1 = _extract_json_from_text(test1)
    assert result1["action"] == "chat"
    assert "Hello" in result1["message"]
    print("✅ Test 1 passed: Preamble/epilogue extraction")
    
    # Test case 2: nested JSON with final answer
    test2 = """Response:

{
  "action": "final",
  "answer": "Python is a programming language"
}

End of response."""
    
    result2 = _extract_json_from_text(test2)
    assert result2["action"] == "final"
    assert "Python" in result2["answer"]
    print("✅ Test 2 passed: Final answer extraction")
    
    # Test case 3: tool call JSON
    test3 = """Here's the tool call:

{
  "action": "tool",
  "tool_name": "sql",
  "input": "SELECT * FROM users"
}

Hope this helps!"""
    
    result3 = _extract_json_from_text(test3)
    assert result3["action"] == "tool"
    assert result3["tool_name"] == "sql"
    print("✅ Test 3 passed: Tool call extraction")
    
    # Test case 4: clean JSON (no extra text)
    test4 = '{"action": "final", "answer": "42"}'
    
    result4 = _extract_json_from_text(test4)
    assert result4["action"] == "final"
    print("✅ Test 4 passed: Clean JSON extraction")
    
    print("\n✅ All tests passed! JSON extraction fix is working correctly.")

if __name__ == "__main__":
    test_json_extraction()
