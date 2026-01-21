import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetHierarchiesInput(BaseModel):
    job_manager_id: str = Field(..., description="The UUID of the job manager to filter hierarchies.")

@tool(args_schema=GetHierarchiesInput)
def get_hierarchies(job_manager_id: str) -> str:
    """Retrieves the list of hierarchies for a specific job manager from the QA environment."""
    # Robustness: Clean the ID if the agent passed "job_manager_id: <uuid>" string
    if job_manager_id and isinstance(job_manager_id, str):
        job_manager_id = job_manager_id.replace("job_manager_id:", "").replace("job_manager_id=", "").strip()
        # Clean any JSON-like syntax if it crept in incorrectly
        job_manager_id = job_manager_id.replace("{", "").replace("}", "").replace('"', "").replace("'", "").strip()

    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/common-hierarchies"
    params = {"job_manager_id": job_manager_id}
    
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
        
        common_hierarchies = data.get("common_hierarchies", [])
        if not common_hierarchies:
            return "No hierarchies found."

        result = []
        
        def parse_hierarchies(h_list):
            for h in h_list:
                result.append({
                    "id": h.get("id"),
                    "name": h.get("name")
                })
                # Check for nested hierarchies
                sub_h = h.get("hierarchies", [])
                if sub_h:
                    parse_hierarchies(sub_h)

        parse_hierarchies(common_hierarchies)
        
        # CACHE THE RESULT
        # cache_tool_result removed as it is not defined

        return json.dumps({"hierarchies": result})
    except Exception as e:
        return f"Error fetching hierarchies: {str(e)}"
