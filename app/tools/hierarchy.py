import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id, request_user_id
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
    user_id = request_user_id.get()
    program_id = request_program_id.get()

    # The hierarchy defaults API is user-specific and starts with /user/program/
    base_url = settings.API_BASE_URL.replace("/api/program", "/api/user/program")
    url = f"{base_url}/{program_id}?is_enabled=true&status=active&user_id={user_id}"
    # params = {"job_manager_id": job_manager_id}
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'origin': 'https://qa-hiring.simplifysandbox.net',
        'referer': 'https://qa-hiring.simplifysandbox.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }

    try:
        print(f"DEBUG: Calling Hierarchy API: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        users = data.get("users", [])
        if not users:
            return "No hierarchies found."

        user = users[0]
        default_h = user.get("default_hierarchy_id", {})
        default_w = user.get("default_work_location_id", {})

<<<<<<< HEAD
        return json.dumps({
            "hierarchie_id": default_h.get("id"),
            "primary_id": default_h.get("id"), # Map primary id same as hierarchy
            "hierarchy_name": default_h.get("name"),
            "currency": default_h.get("default_currency"),
            "work_location_id": default_w.get("id"),
            "location": default_w.get("name"),
            "country_name": default_w.get("country_name"),
            "managed_by": f"{user.get('user_type')}-managed" if user.get("user_type") else "self-managed"
        })
=======
        parse_hierarchies(common_hierarchies)
        
        # CACHE THE RESULT
        # cache_tool_result removed as it is not defined

        return json.dumps({"hierarchies": result})
>>>>>>> 8c43841a5f9220c259199e98fc9ddc046e1669f2
    except Exception as e:
        return f"Error fetching hierarchies: {str(e)}"
