# Model Switching Guide

Mini Devin now supports multiple LLM models. Choose the best one for your use case!

## Available Models

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| **llama3** (8B) | 🐢 30-180s | ⭐⭐⭐⭐⭐ Excellent | Complex queries, accuracy-critical tasks |
| **mistral** (7B) | ⚡ 5-15s | ⭐⭐⭐⭐ Good | General queries, quick responses |
| **neural-chat** (7B) | ⚡ 5-15s | ⭐⭐⭐⭐ Good | Conversations, chat-based interactions |

## How to Switch Models

### Option 1: Environment Variable (Recommended)

**Windows PowerShell:**
```powershell
# For Mistral (fastest)
$env:MINI_DEVIN_MODEL = "mistral"

# For Llama3 (most accurate)
$env:MINI_DEVIN_MODEL = "llama3"

# For Neural Chat
$env:MINI_DEVIN_MODEL = "neural-chat"

# Then start the backend
python run_backend.py
```

**Windows Command Prompt:**
```cmd
set MINI_DEVIN_MODEL=mistral
python run_backend.py
```

**Linux/macOS:**
```bash
export MINI_DEVIN_MODEL=mistral
python run_backend.py
```

### Option 2: Edit Config File

Edit `config.py` and change the default:

```python
# Line 11 in config.py
MODEL = os.getenv("MINI_DEVIN_MODEL", "mistral")  # Change "llama3" to "mistral"
```

### Option 3: Create a Batch Script (Windows)

Create `start_backend_mistral.bat`:
```batch
@echo off
set MINI_DEVIN_MODEL=mistral
call .venv\Scripts\activate.bat
python run_backend.py
```

Then double-click to run.

## Download Models (First Time Only)

Before using a model, download it with Ollama:

```bash
# Download Mistral
ollama pull mistral

# Download Neural Chat
ollama pull neural-chat

# Llama3 (usually already installed)
ollama pull llama3
```

## Quick Start: Switch to Mistral

**Fastest way to switch (PowerShell):**

```powershell
# 1. Download mistral (one-time)
ollama pull mistral

# 2. Set environment variable
$env:MINI_DEVIN_MODEL = "mistral"

# 3. Start backend
python run_backend.py

# You should see in logs:
# "LLM Model: Mistral (7B) | Speed: Fast (5-15s) | Accuracy: Good"
```

**Then test the API:**

```bash
curl "http://127.0.0.1:8001/agent?query=What%20is%20Python?"
```

Expected response time: **5-15 seconds** (vs 30-180s with llama3)

## Performance Comparison

### Before (llama3)
```
Request: "What is Python?"
Time: 180.40s ❌
```

### After (mistral)
```
Request: "What is Python?"
Time: 8.5s ✅
```

**Speed improvement: ~21x faster!**

## Model Recommendations

### Use Mistral When:
- ✅ You want fast responses (< 15 seconds)
- ✅ Running on CPU/older hardware
- ✅ You don't need maximum accuracy
- ✅ Testing/development environment

### Use Llama3 When:
- ✅ You need the most accurate answers
- ✅ Working on complex tasks
- ✅ Running on GPU (will be much faster)
- ✅ Production environment with hardware budget

### Use Neural Chat When:
- ✅ Conversational responses
- ✅ Multi-turn dialog
- ✅ Similar speed to Mistral, optimized for chat

## Check Current Model

```bash
python config.py
```

Output:
```
============================================================
Mini Devin LLM Configuration
============================================================
Active Model:  Mistral (7B)
Speed:         Fast (5-15s)
Accuracy:      Good
Best for:      Quick responses, general queries
============================================================
```

## Troubleshooting

### Model not found error
```
Error: No model named 'mistral'
```
**Fix:** Download the model first with `ollama pull mistral`

### Still slow after switching
- Check if Ollama is running: `ollama serve`
- Verify environment variable: `echo $env:MINI_DEVIN_MODEL` (PowerShell)
- Check logs for which model is being used

### Want to go back to Llama3
```powershell
$env:MINI_DEVIN_MODEL = "llama3"
python run_backend.py
```

---

**Recommended setup for most users: Use Mistral for 7-21x faster responses!** ⚡
