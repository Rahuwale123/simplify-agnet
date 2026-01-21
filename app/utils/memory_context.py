from typing import Dict
from langchain.memory import ConversationBufferMemory

_user_memories: Dict[str, ConversationBufferMemory] = {}


def get_user_memory(user_id: str) -> ConversationBufferMemory:
    """
    Get or create ConversationBufferMemory for a user_id.
    """
    if user_id not in _user_memories:
        _user_memories[user_id] = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )

    return _user_memories[user_id]


def clear_user_memory(user_id: str) -> None:
    """
    Clear conversation memory for a specific user.
    """
    if user_id in _user_memories:
        _user_memories[user_id].clear()
