"""
Configuration for Mini Devin AI Assistant.

Model options:
- "llama3" (8B) - Most accurate, slower (~30-180s per query)
- "mistral" (7B) - Fast, good accuracy (~5-15s per query)
- "neural-chat" (7B) - Optimized for chat, fast (~5-15s per query)
"""

import os

# Get model from environment or use default
# Options: "llama3", "mistral", "neural-chat"
MODEL = os.getenv("MINI_DEVIN_MODEL", "llama3")

# Validate model choice
AVAILABLE_MODELS = {
    "llama3": {
        "name": "Llama 3 (8B)",
        "speed": "Slow (30-180s)",
        "accuracy": "Excellent",
        "best_for": "Accuracy-critical tasks"
    },
    "mistral": {
        "name": "Mistral (7B)",
        "speed": "Fast (5-15s)",
        "accuracy": "Good",
        "best_for": "Quick responses, general queries"
    },
    "neural-chat": {
        "name": "Neural Chat (7B)",
        "speed": "Fast (5-15s)",
        "accuracy": "Good",
        "best_for": "Chat and conversation"
    }
}

if MODEL not in AVAILABLE_MODELS:
    raise ValueError(
        f"Invalid model '{MODEL}'. Available: {list(AVAILABLE_MODELS.keys())}"
    )

# Request timeout (seconds)
LLM_REQUEST_TIMEOUT = 120  # Increase to 120s to handle slow models

# Cache settings
CACHE_MAX_SIZE = 100
TOOL_CACHE_MAX_SIZE = 200

# Agent settings
MAX_AGENT_STEPS = 3

def get_model_info() -> dict:
    """Get information about the current model."""
    return {
        "model": MODEL,
        **AVAILABLE_MODELS[MODEL]
    }

def print_model_info():
    """Print current model configuration."""
    info = get_model_info()
    print("\n" + "="*60)
    print("Mini Devin LLM Configuration")
    print("="*60)
    print(f"Active Model:  {info['name']}")
    print(f"Speed:         {info['speed']}")
    print(f"Accuracy:      {info['accuracy']}")
    print(f"Best for:      {info['best_for']}")
    print("="*60 + "\n")

if __name__ == "__main__":
    print_model_info()
