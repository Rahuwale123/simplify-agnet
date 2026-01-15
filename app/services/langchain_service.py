from app.agents.base_agent import create_agent, get_history_string, add_message
from typing import Dict, AsyncGenerator
import asyncio
from app.utils.callbacks import StatusCallbackHandler

# Dictionary to store agent executors per user to maintain isolated *executor* instances
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
        
        # Get Current History
        history_str = get_history_string(user_id)
        
        # Run agent in background task
        # Pass chat_history in input
        task = asyncio.create_task(
            agent_executor.ainvoke(
                {
                    "input": message,
                    "chat_history": history_str
                }, 
                config={"callbacks": [callback]}
            )
        )
        
        # Consume queue while task is running
        queue_task = None
        while not task.done():
            try:
                # Create a task for getting the next message if one isn't running
                if queue_task is None:
                    queue_task = asyncio.create_task(queue.get())

                # Wait for either new message or agent completion
                done, pending = await asyncio.wait(
                    [queue_task, task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                if queue_task in done:
                    # Message received
                    msg = queue_task.result()
                    yield f"{msg}\n\n"
                    queue_task = None # Reset so we create a new one next loop
                
                if task in done:
                    # Agent finished
                    # If queue_task is still pending, we should cancel it or let it finish if strict
                    if queue_task and not queue_task.done():
                        queue_task.cancel()
                        try:
                            await queue_task
                        except asyncio.CancelledError:
                            pass
                    break
                    
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
        
        # SAVE TO MEMORY
        add_message(user_id, "user", message)
        add_message(user_id, "ai", output)
        
        yield f"result:{output}\n\n"
        
    except Exception as e:
        yield f"error:{str(e)}\n\n"
