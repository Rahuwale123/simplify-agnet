from app.agents.base_agent import create_agent, add_message
from typing import Dict, AsyncGenerator
import asyncio
from app.utils.callbacks import StatusCallbackHandler
from app.services.history_adapter import SQLiteHistoryAdapter
from langchain_core.messages import HumanMessage, AIMessage

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
        # 1. Get or Create Agent Executor
        if user_id not in user_agents:
            user_agents[user_id] = create_agent(user_id)
        
        agent_executor = user_agents[user_id]
        
        # 2. Setup Callbacks
        queue = asyncio.Queue()
        callback = StatusCallbackHandler(queue)
        
        # 3. Initialize History Adapter & Fetch Context
        adapter = SQLiteHistoryAdapter(user_id)
        history = adapter.messages # List[BaseMessage]
        print(f"DEBUG: History loaded. Types: {[type(m) for m in history]}")
        
        # 4. Define Agent Task (Manual History Injection)
        async def agent_task():
            import traceback
            try:
                # Invoke Agent
                print("DEBUG: Invoking agent...")
                result = await agent_executor.ainvoke(
                    {
                        "input": message,
                        "chat_history": history
                    }, 
                    config={"callbacks": [callback]}
                )
                print("DEBUG: Agent invoked successfully.")
                
                # Manual Persistence (Save User Input & AI Output)
                # Note: We save AFTER success to avoid saving failed interactions? 
                # Or BEFORE to ensure prompt logging? 
                # Std is save Input before, Output after. Adapter.add_message handles simple checking.
                adapter.add_message(HumanMessage(content=message))
                
                output_text = str(result["output"])
                adapter.add_message(AIMessage(content=output_text))

                # Save Tool Outputs (Intermediate Steps)
                if "intermediate_steps" in result:
                    for action, observation in result["intermediate_steps"]:
                        # Convert tool output to string log
                        log_entry = f"Tool '{action.tool}' returned: {observation}"
                        # Use helper that wraps db_service
                        add_message(user_id, "tool", log_entry)
                
                return result
            except (StopIteration, StopAsyncIteration):
                # Handle iterator exhaustion gracefully (treat as empty finish)
                await queue.put("Agent stopped unexpectedly (StopIteration).")
                return {"output": "Agent stopped unexpectedly."}
            except Exception as e:
                # Put error in queue so consumer sees it
                await queue.put(f"Error executing agent: {str(e)}")
                raise e

        # Run agent in background task
        task = asyncio.create_task(agent_task())
        
        # 5. Queue Consumer Loop
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
        
        # Strip trailing newlines and replace internal newlines with spaces
        # This prevents both truncation (SSE validation) and visible "\n" artifacts
        safe_output = output.strip().replace("\n", "  ")

        yield f"result:{safe_output}\n\n"
        
    except Exception as e:
        yield f"error:{str(e)}\n\n"
