import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings
from app.tools.memory_tools import cache_tool_result

class GetJobManagersInput(BaseModel):
    page: int = Field(1, description="Page number for pagination.")
    limit: int = Field(25, description="Limit of items per page.")

@tool(args_schema=GetJobManagersInput)
def get_job_managers(page: int = 1, limit: int = 25) -> str:
    """Retrieves a list of available job managers from the QA environment."""
    token = request_token.get()
    program_id = request_program_id.get()

    # Note: URL contains the typo 'manegers' as per user requirement
    url = f"{settings.API_BASE_URL}/{program_id}/get-job-manegers"
    params = {"page": page, "limit": limit}
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'origin': 'https://qa-hiring.simplifysandbox.net',
        'referer': 'https://qa-hiring.simplifysandbox.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        users = data.get("users", [])
        if not users:
            return "No job managers found."

        result = []
        for u in users:
            first_name = u.get("first_name", "")
            last_name = u.get("last_name", "")
            manager_id = u.get("user_id", "")
            result.append({
                "id": manager_id,
                "name": f"{first_name} {last_name}".strip()
            })

        # CACHE THE RESULT for 'get_last_search'
        cache_tool_result("managers", result)

        return json.dumps({"managers": result})
    except Exception as e:
        return f"Error fetching job managers: {str(e)}"
