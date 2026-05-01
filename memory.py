from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mini_devin"]
collection = db["chat_memory"]

def save_message(user, message, response):
    collection.insert_one({
        "user": user,
        "message": message,
        "response": response,
        "created_at": datetime.utcnow()
    })

def _serialize_document(doc):
    return {
        "id": str(doc["_id"]),
        "user": doc.get("user"),
        "message": doc.get("message"),
        "response": doc.get("response"),
        "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None
    }


def delete_history():
    result = collection.delete_many({})
    return result.deleted_count


def get_history(limit=10):
    docs = collection.find().sort("_id", -1).limit(limit)
    return [_serialize_document(doc) for doc in docs]