import redis
import os
import json
from typing import List, Dict

class RedisService:
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', '150.241.245.84')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = 0
        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """Retrieves default chat history for a session."""
        try:
            key = f"chat_history:{session_id}"
            messages = self.client.lrange(key, 0, -1)
            return [json.loads(m) for m in messages]
        except Exception as e:
            print(f"Redis Error (get_history): {e}")
            return []

    def get_first_message(self, session_id: str) -> str:
        """Retrieves only the first message content from history for use as a title."""
        try:
            key = f"chat_history:{session_id}"
            first_msg = self.client.lindex(key, 0)
            if first_msg:
                data = json.loads(first_msg)
                # Try to return first user message if possible, or just first message
                return data.get("content", "New Chat")
            return "New Chat"
        except Exception as e:
            print(f"Redis Error (get_first_message): {e}")
            return "New Chat"

    def add_message(self, session_id: str, role: str, content: str):
        """Appends a message to the session history."""
        try:
            key = f"chat_history:{session_id}"
            message = json.dumps({"role": role, "content": content})
            self.client.rpush(key, message)
        except Exception as e:
            print(f"Redis Error (add_message): {e}")

    def clear_history(self, session_id: str):
        """Clears the history for a session."""
        try:
            key = f"chat_history:{session_id}"
            self.client.delete(key)
        except Exception as e:
            print(f"Redis Error (clear_history): {e}")

# Singleton instance
redis_service = RedisService()
