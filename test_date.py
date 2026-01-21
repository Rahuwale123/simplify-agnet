import asyncio
from app.tools.date_tools import get_current_date
from langchain.agents import AgentExecutor
from langchain.agents.tool import Tool

async def test():
    print("Testing tool direct call:")
    try:
        # It's a structured tool, so we call .invoke
        print(get_current_date.invoke({}))
    except Exception as e:
        print(f"Direct call empty dict failed: {e}")

    try:
        print(get_current_date.invoke(""))
    except Exception as e:
        print(f"Direct call empty string failed: {e}")

    try:
        print(get_current_date.invoke({"input": ""}))
    except Exception as e:
        print(f"Direct call input dict failed: {e}")


if __name__ == "__main__":
    asyncio.run(test())
