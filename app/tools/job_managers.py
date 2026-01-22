import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetJobManagersInput(BaseModel):
    page: Optional[int] = Field(1, description="Page number for pagination.")
    limit: Optional[int] = Field(25, description="Limit of items per page.")

@tool(args_schema=GetJobManagersInput)
def get_job_managers(page: Optional[int] = 1, limit: Optional[int] = 25) -> str:
    """Retrieves available job managers. Matches current user ID for auto-selection."""
    # Handle Robustness if agent sends empty string or None
    if page is None or (isinstance(page, str) and not str(page).isdigit()):
        page = 1
    if limit is None or (isinstance(limit, str) and not str(limit).isdigit()):
        limit = 25
    page = int(page)
    limit = int(limit)
    from app.utils.context import request_token, request_program_id, request_user_id
    token = request_token.get()
    program_id = request_program_id.get()
    current_user_id = request_user_id.get()

    # Note: URL contains the typo 'manegers' as per user requirement
    # If this also needs /user/ prefix due to 403, we could change it, but the hierarchy cURL was explicit for defaults.
    url = f"{settings.API_BASE_URL}/{program_id}/get-job-manegers"
    params = {"page": page, "limit": limit}
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        users = data.get("users", [])
        if not users:
            return "No job managers found."

        # logic: find if current_user_id is in the list
        matched_manager = None
        all_managers = []
        
        for u in users:
            manager_id = u.get("user_id", "")
            manager_name = f"{u.get('first_name', '')} {u.get('last_name', '')}".strip()
            
            mgr_data = {"id": manager_id, "name": manager_name}
            all_managers.append(mgr_data)
            
            if manager_id == current_user_id:
                matched_manager = mgr_data

        if matched_manager:
            return json.dumps({
                "selection": "auto",
                "manager": matched_manager,
                "message": f"I've automatically selected you ({matched_manager['name']}) as the Job Manager."
            })

        return json.dumps({"managers": all_managers})
    except Exception as e:
        return f"Error fetching job managers: {str(e)}"
