from app.agents.base_agent import create_agent
from typing import Dict, AsyncGenerator
import asyncio
from app.utils.callbacks import StatusCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage
from app.services.redis_service import redis_service

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
        
        # 3. Load History from Redis
        raw_history = redis_service.get_history(user_id)
        chat_history = []
        for msg in raw_history:
            if msg["role"] == "user":
                chat_history.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "ai":
                chat_history.append(AIMessage(content=msg["content"]))
                
        # Save User Message immediately
        redis_service.add_message(user_id, "user", message)
        
        # 4. Define Agent Task
        async def agent_task():
            try:
                # Invoke Agent
                print(f"DEBUG: Invoking agent (History Length: {len(chat_history)})...")
                result = await agent_executor.ainvoke(
                    {
                        "input": message,
                        "chat_history": chat_history
                    }, 
                    config={"callbacks": [callback]}
                )
                print("DEBUG: Agent invoked successfully.")
                
                # Save AI Output
                if "output" in result:
                     redis_service.add_message(user_id, "ai", result["output"])
                
                return result
            except (StopIteration, StopAsyncIteration):
                await queue.put("Agent stopped unexpectedly (StopIteration).")
                return {"output": "Agent stopped unexpectedly."}
            except Exception as e:
                await queue.put(f"Error executing agent: {str(e)}")
                raise e

        # Run agent in background task
        task = asyncio.create_task(agent_task())
        
        # 5. Queue Consumer Loop
        queue_task = None
        while not task.done():
            try:
                if queue_task is None:
                    queue_task = asyncio.create_task(queue.get())

                done, pending = await asyncio.wait(
                    [queue_task, task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                if queue_task in done:
                    msg = queue_task.result()
                    yield f"{msg}\n\n"
                    queue_task = None
                
                if task in done:
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
            
        if task.exception():
            raise task.exception()
            
        result = await task
        output = result["output"]
        
        safe_output = output.strip().replace("\n", "  ")
        yield f"result:{safe_output}\n\n"
        
    except Exception as e:
        yield f"error:{str(e)}\n\n"
