from app.agents.base_agent import create_agent
from typing import Dict, AsyncGenerator
import asyncio
from app.utils.callbacks import StatusCallbackHandler

# Dictionary to store agent executors per user to maintain isolated memory
user_agents: Dict[str, any] = {}

async def run_agent(message: str, user_id: str) -> AsyncGenerator[str, None]:
    """
    Runs the agent and yields status updates and the final result.
    Yields strings formatted as SSE data:
    "status: <message>"
    "result: <final_text>"
    """
    try:
        # Create a new agent for the user if it doesn't exist
        if user_id not in user_agents:
            user_agents[user_id] = create_agent(user_id)
        
        agent_executor = user_agents[user_id]
        
        # Queue for status updates
        queue = asyncio.Queue()
        callback = StatusCallbackHandler(queue)
        
        # Run agent in background task
        task = asyncio.create_task(
            agent_executor.ainvoke(
                {"input": message}, 
                config={"callbacks": [callback]}
            )
        )
        
        # Consume queue while task is running
        while not task.done():
            try:
                # Wait for next item or task completion
                # We use a small timeout to check task status frequently
                # or we can wait for both queue.get() and task
                done, pending = await asyncio.wait(
                    [asyncio.create_task(queue.get()), task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                for t in done:
                    if t is task:
                        # Task finished
                        pass
                    else:
                        # Queue item available
                        msg = t.result()
                        yield f"{msg}\n\n"
            except Exception:
                break
                
        # Flush remaining queue items
        while not queue.empty():
            msg = await queue.get()
            yield f"{msg}\n\n"
            
        # Get final result
        if task.exception():
            raise task.exception()
            
        result = await task
        output = result["output"]
        yield f"result:{output}\n\n"
        
    except Exception as e:
        yield f"error:{str(e)}\n\n"
