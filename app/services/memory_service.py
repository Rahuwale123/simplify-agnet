import redis
import os
import json

class MemoryService:
    @staticmethod
    def get_messages(session_id: str):
        try:
            r = redis.Redis(
                host=os.getenv('REDIS_HOST', '150.241.245.84'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=0,
                decode_responses=True
            )
            # Assuming chat history is stored as a list of JSON strings at key "chat_history:{session_id}"
            # This is a common pattern. Adjust if Simi AI uses a different key schema.
            key = f"chat_history:{session_id}"
            messages = r.lrange(key, 0, -1)
            return [json.loads(m) for m in messages]
        except Exception as e:
            print(f"Error fetching from Redis: {e}")
            return []

def clear_chat_history(session_id: str):
    """Clears the chat history for a specific session."""
    try:
        r = redis.Redis(
            host=os.getenv('REDIS_HOST', '150.241.245.84'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=True
        )
        key = f"chat_history:{session_id}"
        r.delete(key)
        print(f"Cleared history for session: {session_id}")
    except Exception as e:
        print(f"Error clearing Redis history: {e}")
