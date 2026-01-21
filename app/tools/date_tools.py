from langchain.tools import tool
import datetime
import json

@tool
def get_current_date(query: str = "") -> str:
    """
    This tool retrieves the current system date and year.
    It should be called whenever the user asks any question related to dates or time.
    The returned current date must be used as the reference to resolve the user's query accurately.
    """
    today = datetime.datetime.now()
    return json.dumps({"current_date": today.strftime("%Y-%m-%d"), "year": today.year})
