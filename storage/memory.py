from datetime import datetime
from pymongo import MongoClient
import logging
import time

logger = logging.getLogger('storage')

# Initialize MongoDB connection
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mini_devin"]
    collection = db["chat_memory"]
    logger.info("MongoDB connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}", exc_info=True)
    raise

def save_message(user, message, response):
    """Save a chat message to MongoDB."""
    logger.info(f"Saving message for user: {user}",
                extra={'extra_fields': {
                    'user': user,
                    'message_length': len(message),
                    'response_length': len(response)
                }})

    start_time = time.time()

    try:
        doc = {
            "user": user,
            "message": message,
            "response": response,
            "created_at": datetime.utcnow()
        }

        result = collection.insert_one(doc)
        process_time = time.time() - start_time

        logger.info(f"Message saved successfully in {process_time:.3f}s",
                   extra={'extra_fields': {
                       'process_time': f"{process_time:.3f}s",
                       'document_id': str(result.inserted_id)
                   }})

        return str(result.inserted_id)

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Failed to save message after {process_time:.3f}s: {str(e)}",
                    extra={'extra_fields': {'process_time': f"{process_time:.3f}s"}},
                    exc_info=True)
        raise

def _serialize_document(doc):
    """Convert MongoDB document to serializable format."""
    try:
        return {
            "id": str(doc["_id"]),
            "user": doc.get("user"),
            "message": doc.get("message"),
            "response": doc.get("response"),
            "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None
        }
    except Exception as e:
        logger.error(f"Failed to serialize document: {str(e)}", exc_info=True)
        return None

def delete_history():
    """Delete all chat history from MongoDB."""
    logger.info("Deleting all chat history")

    start_time = time.time()

    try:
        result = collection.delete_many({})
        deleted_count = result.deleted_count
        process_time = time.time() - start_time

        logger.info(f"Chat history cleared in {process_time:.3f}s: {deleted_count} records deleted",
                   extra={'extra_fields': {
                       'process_time': f"{process_time:.3f}s",
                       'records_deleted': deleted_count
                   }})

        return deleted_count

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Failed to delete history after {process_time:.3f}s: {str(e)}",
                    extra={'extra_fields': {'process_time': f"{process_time:.3f}s"}},
                    exc_info=True)
        raise

def get_history(limit=10):
    """Retrieve chat history from MongoDB."""
    logger.info(f"Retrieving chat history: limit={limit}",
                extra={'extra_fields': {'limit': limit}})

    start_time = time.time()

    try:
        docs = list(collection.find().sort("_id", -1).limit(limit))
        serialized_docs = [_serialize_document(doc) for doc in docs if doc is not None]
        # Filter out None values from serialization failures
        serialized_docs = [doc for doc in serialized_docs if doc is not None]

        process_time = time.time() - start_time

        logger.info(f"Chat history retrieved in {process_time:.3f}s: {len(serialized_docs)} records",
                   extra={'extra_fields': {
                       'process_time': f"{process_time:.3f}s",
                       'records_returned': len(serialized_docs)
                   }})

        return serialized_docs

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Failed to retrieve history after {process_time:.3f}s: {str(e)}",
                    extra={'extra_fields': {'process_time': f"{process_time:.3f}s"}},
                    exc_info=True)
        raise
