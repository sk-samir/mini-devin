from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from llm.llm import ask_llm, explain_code
from storage.memory import save_message, get_history, delete_history
from agents.sql_agent import ask_database
from agents.agent import agent_loop
import logging_config
from config import get_model_info
import time
import logging

# Initialize logging
logging_config.init_logging()
logger = logging.getLogger('api')

app = FastAPI(
    title="Mini Devin API",
    description="AI Agent API with LLM, SQL, and Code Explanation capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Request started: {request.method} {request.url.path}",
                extra={
                    'extra_fields': {
                        'method': request.method,
                        'path': request.url.path,
                        'query_params': str(request.query_params),
                        'client_ip': request.client.host if request.client else None
                    }
                })

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(f"Request completed: {request.method} {request.url.path} - Status: {response.status_code}",
                    extra={
                        'extra_fields': {
                            'status_code': response.status_code,
                            'process_time': f"{process_time:.3f}s"
                        }
                    })

        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {request.method} {request.url.path} - Error: {str(e)}",
                     extra={
                         'extra_fields': {
                             'process_time': f"{process_time:.3f}s",
                             'error_type': type(e).__name__
                         }
                     },
                     exc_info=True)
        raise

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Mini Devin API starting up")
    
    # Log model configuration
    model_info = get_model_info()
    logger.info(f"LLM Model: {model_info['name']} | Speed: {model_info['speed']} | Accuracy: {model_info['accuracy']}")
    
    logger.info("Available endpoints:")
    for route in app.routes:
        if hasattr(route, 'path'):
            logger.info(f"  {route.path}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Mini Devin API shutting down")

@app.get("/agent")
def agent(query: str):
    """Run the AI agent with the given query."""
    try:
        logger.info(f"Agent request received: {query[:100]}...")
        start_time = time.time()

        result = agent_loop(query)

        process_time = time.time() - start_time
        logger.info(f"Agent request completed in {process_time:.2f}s",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s"}})

        return {"query": query, "result": result}

    except Exception as e:
        logger.error(f"Agent request failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/ask")
def ask(question: str):
    """Ask the LLM a question and save to chat history."""
    try:
        logger.info(f"LLM question received: {question[:100]}...")
        start_time = time.time()

        response = ask_llm(question)
        save_message("user", question, response)

        process_time = time.time() - start_time
        logger.info(f"LLM question answered in {process_time:.2f}s",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s"}})

        return {"question": question, "response": response}

    except Exception as e:
        logger.error(f"LLM question failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

@app.get("/explain")
def explain(code: str):
    """Explain the provided code using LLM."""
    try:
        logger.info(f"Code explanation request received: {len(code)} characters")
        start_time = time.time()

        explanation = explain_code(code)

        process_time = time.time() - start_time
        logger.info(f"Code explanation completed in {process_time:.2f}s",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s"}})

        return {"code": code, "explanation": explanation}

    except Exception as e:
        logger.error(f"Code explanation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Code explanation error: {str(e)}")

@app.get("/history")
def history(limit: int = 20):
    """Get chat history from database."""
    try:
        logger.info(f"History request received: limit={limit}")
        start_time = time.time()

        history_data = get_history(limit)

        process_time = time.time() - start_time
        logger.info(f"History retrieved in {process_time:.2f}s: {len(history_data)} records",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s", 'records_count': len(history_data)}})

        return history_data

    except Exception as e:
        logger.error(f"History retrieval failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"History error: {str(e)}")

@app.delete("/history")
def clear_history():
    """Clear all chat history from database."""
    try:
        logger.info("History clear request received")
        start_time = time.time()

        deleted = delete_history()

        process_time = time.time() - start_time
        logger.info(f"History cleared in {process_time:.2f}s: {deleted} records deleted",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s", 'records_deleted': deleted}})

        return {"deleted": deleted, "status": "ok"}

    except Exception as e:
        logger.error(f"History clear failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"History clear error: {str(e)}")

@app.get("/sql")
def sql(question: str):
    """Convert natural language question to SQL and execute."""
    try:
        logger.info(f"SQL request received: {question[:100]}...")
        start_time = time.time()

        result = ask_database(question)

        process_time = time.time() - start_time
        logger.info(f"SQL query completed in {process_time:.2f}s",
                    extra={'extra_fields': {'process_time': f"{process_time:.2f}s"}})

        return result

    except Exception as e:
        logger.error(f"SQL request failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"SQL error: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

