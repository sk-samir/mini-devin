# Performance Analysis: `/agent?query=What%20is%20Python?` Slowness

## 🔴 Root Cause: LLM Inference Time

Recent request timing (2026-05-04 19:01:40):
- **Total time**: 180.40 seconds (~3 minutes)
- **Breakdown**: Almost entirely due to Ollama/llama3 inference

Historical LLM response times:
- 639.09s (10+ minutes) ⚠️ 
- 115.83s
- 68.37s
- 57.87s
- 48.86s
- 36.85s
- 34.86s
- 12.73s (best case)

## 🎯 Why It's Slow

1. **Large Model Size**: `llama3` is a 7-8B parameter model
   - Very accurate but computationally expensive
   - Not designed for low-latency responses

2. **CPU-based Inference**: No GPU acceleration detected
   - Ollama running on CPU (likely)
   - Model inference on CPU = slow

3. **No Streaming**: Full response must complete before returning
   - User sees nothing until entire answer is ready
   - Feels like app is frozen

4. **Request Blocking**: Synchronous `ollama.chat()` calls
   - Backend thread blocked while waiting for LLM
   - Can't handle concurrent requests efficiently

## 📊 Performance Bottlenecks

### In `/agent?query=...`
```
User Request
    ↓
FastAPI endpoint (< 1ms)
    ↓
agent_loop()
    ├─ get_history() (0.001-0.03s) ✅ Fast
    ├─ Build context (< 1ms) ✅ Fast
    ├─ ollama.chat() (12-639s) 🔴 SLOW
    │   └─ llama3 inference (entire delay)
    └─ Return response
```

## 💡 Solutions (Ranked by Impact)

### 1. **Switch to Faster Model** (Biggest Impact)
Replace `llama3` with a smaller, faster model:

| Model | Params | Speed | Accuracy | Use Case |
|-------|--------|-------|----------|----------|
| orca-mini | 3B | ⚡⚡⚡ (1-5s) | Good | Quick answers |
| neural-chat | 7B | ⚡⚡ (5-15s) | Good | Balanced |
| mistral | 7B | ⚡⚡ (5-15s) | Excellent | Best balance |
| dolphin-mixtral | 8x7B | ⚡ (10-30s) | Excellent | Complex queries |
| llama3 | 8B | 🐢 (30-120s+) | Excellent | Current (slow) |

**Recommended**: Switch to `mistral` or `neural-chat` for 3-4x speedup

### 2. **Enable GPU Acceleration** 
If GPU available (NVIDIA/AMD):
```powershell
$env:OLLAMA_DEVICE = "cuda"  # NVIDIA GPU
# or
$env:OLLAMA_DEVICE = "rocm"  # AMD GPU
ollama serve
```
Expected speedup: **5-10x faster**

### 3. **Add Response Streaming**
Stream partial responses to user while LLM is still generating:
```python
@app.get("/agent/stream")
async def agent_stream(query: str):
    # Stream tokens as they arrive
    # User sees response building in real-time
```

### 4. **Implement Request Timeout + Fallback**
```python
def agent_loop(user_input: str, max_steps=3, timeout=30):
    # If LLM takes > 30s, return cached/approximated answer
```

### 5. **Use LLM Response Caching**
Already implemented in `agents/agent.py` but:
- Cache key based on query + history
- Simple queries might hit same combinations

### 6. **Batch Processing & Queue**
- Process multiple requests asynchronously
- Don't block on individual LLM calls

## 🔧 Immediate Fix: Switch to Faster Model

### Steps to implement:

1. **Pull faster model**:
```powershell
ollama pull mistral
# or
ollama pull neural-chat
```

2. **Update `llm/llm.py`**:
```python
# Change from:
response = ollama.chat(model="llama3", ...)
# To:
response = ollama.chat(model="mistral", ...)
```

3. **Update `agents/agent.py`**:
```python
response = ollama.chat(model="mistral", ...)
```

4. **Test**:
```bash
curl "http://127.0.0.1:8001/agent?query=What%20is%20Python?"
# Should now complete in 10-20 seconds instead of 180s
```

## 📈 Expected Results After Fixes

| Change | Time | vs Current |
|--------|------|-----------|
| Current (llama3 CPU) | ~180s | Baseline |
| Switch to Mistral | ~15-25s | **7-12x faster** ✅ |
| Mistral + GPU | ~3-8s | **22-60x faster** ✅✅ |
| Mistral + GPU + Streaming | ~3-8s | Same speed, better UX |

## 📋 Recommended Action Plan

1. **Week 1**: Switch to Mistral (quick win, no code changes needed)
2. **Week 2**: Enable GPU if available
3. **Week 3**: Add streaming for better UX
4. **Week 4**: Implement timeout + fallback logic

---

**Note**: The slowness is **NOT** a code issue—it's a model/hardware constraint. Optimization requires either:
- Faster model selection
- Better hardware (GPU)
- Architecture changes (streaming, caching, queuing)
