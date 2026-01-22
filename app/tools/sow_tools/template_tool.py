
import requests
import json
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetJobTemplatesInput(BaseModel):
    hierarchy_id: str = Field(..., description="The Hierarchy ID to filter templates by. This is a mandatory input field.")
    page: int = Field(1, description="Page number for pagination.")
    limit: int = Field(10, description="Number of items per page.")
    is_enabled: bool = Field(True, description="Filter by enabled status. Defaults to True.")

@tool(args_schema=GetJobTemplatesInput)
def get_sow_job_templates(hierarchy_id: str, page: int = 1, limit: int = 10, is_enabled: bool = True) -> str:
    """Retrieves a list of job templates for a specific hierarchy from the QA environment."""
    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/job-template/advance-filter"
    
    # POST request payload based on the curl command
    # Note: Curl shows hierarchy_ids as string "...", but earlier examples used list.
    # The payload shows "hierarchy_ids": "..." which might be a typo in curl or API accepts both.
    # Let's assume list of strings is safer if name is plural, but follow raw closely if needed.
    # Actually, looking at the previous vendor one, it was list. 
    # The curl here says: "hierarchy_ids":"GUID" (string). 
    # I will pass it as a string to match the curl exactly, but usually IDs are lists.
    # Let's try passing as string as per specific curl request provided.
    
    payload = {
        "hierarchy_ids": hierarchy_id, 
        "page": page,
        "limit": limit,
        "is_enabled": is_enabled
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'content-type': 'application/json',
        'origin': 'https://qa-hiring.simplifysandbox.net',
        'referer': 'https://qa-hiring.simplifysandbox.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        return json.dumps(data)
        
    except Exception as e:
        return f"Error fetching job templates: {str(e)}"
