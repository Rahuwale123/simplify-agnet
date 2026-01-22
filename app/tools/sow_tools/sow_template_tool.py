
import requests
import json
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetSowTemplatesInput(BaseModel):
    hierarchy_id: str = Field(..., description="The Hierarchy ID to filter templates by. This is a mandatory field.")
    type_id: str = Field(..., description="The SOW Type ID to filter templates by (e.g. 'eb3b21e2...'). This is a mandatory field.")
    page: int = Field(1, description="Page number for pagination.")
    limit: int = Field(10, description="Number of items per page.")

@tool(args_schema=GetSowTemplatesInput)
def get_sow_templates(hierarchy_id: str, type_id: str, page: int = 1, limit: int = 10) -> str:
    """Retrieves a list of SOW templates for a specific hierarchy and type from the QA environment."""
    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/sow-templates"
    
    params = {
        "page": page,
        "limit": limit,
        "type": type_id,
        "hierarchy_id": hierarchy_id
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'origin': 'https://qa-hiring.simplifysandbox.net',
        'referer': 'https://qa-hiring.simplifysandbox.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        return json.dumps(data)
        
    except Exception as e:
        return f"Error fetching SOW templates: {str(e)}"
