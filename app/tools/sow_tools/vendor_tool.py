
import requests
import json
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetVendorsInput(BaseModel):
    hierarchy_id: str = Field(..., description="The Hierarchy ID to filter vendors by. This is a mandatory field.")
    page: int = Field(1, description="Page number for pagination.")
    status: str = Field("Active", description="Filter by status. Defaults to 'Active'.")
    display_name: str = Field("", description="Filter by display name (partial match). Defaults to empty string.")

@tool(args_schema=GetVendorsInput)
def get_sow_vendors(hierarchy_id: str, page: int = 1, status: str = "Active", display_name: str = "") -> str:
    """Retrieves a list of vendors for a specific hierarchy from the QA environment."""
    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/program-vendor/advance-filter"
    
    # POST request payload based on the curl command
    payload = {
        "hierarchy_ids": [hierarchy_id],
        "page": page,
        "status": status,
        "display_name": display_name
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
        return f"Error fetching vendors: {str(e)}"
