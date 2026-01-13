from app.agents.base_agent import create_agent
from typing import Dict

# Dictionary to store agent executors per user to maintain isolated memory
user_agents: Dict[str, any] = {}

async def run_agent(message: str, user_id: str) -> str:
    try:
        # Create a new agent for the user if it doesn't exist
        if user_id not in user_agents:
            user_agents[user_id] = create_agent(user_id)
        
        agent_executor = user_agents[user_id]
        
        # Pass the message as it is as per user request
        response = await agent_executor.ainvoke({"input": message})
        return response["output"]
    except Exception as e:
        return f"Agent Error: {str(e)}"
