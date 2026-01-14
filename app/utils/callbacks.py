import asyncio
from typing import Any, Dict, List, Union
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import AgentAction

class StatusCallbackHandler(AsyncCallbackHandler):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self.tool_messages = {
            "get_job_managers": "🔍 Finding Job Managers...",
            "get_hierarchies": "🏢 Loading Hierarchies...",
            "get_job_templates": "📋 Fetching Job Templates...",
            "get_source_types": "🧩 Determining Source Types...",
            "save_field": "💾 Saving your selection...",
            "check_missing_fields": "📝 Checking details...",
            "submit_job": "🚀 Submitting Job Draft...",
            "get_draft": "👀 Reviewing draft...",
            "get_current_date": "📅 Checking date..."
        }

    async def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Run when tool starts running."""
        tool_name = serialized.get("name")
        message = self.tool_messages.get(tool_name, f"Working on {tool_name}...")
        await self.queue.put(f"status:{message}")

    async def on_agent_finish(self, finish: Any, **kwargs: Any) -> None:
        """Run on agent end."""
        await self.queue.put("status:Done")
