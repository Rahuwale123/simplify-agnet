
import requests
import json
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetChecklistInput(BaseModel):
    page: int = Field(1, description="Page number for pagination.")
    limit: int = Field(10, description="Limit of items per page.")
    is_enabled: bool = Field(True, description="Filter for enabled checklists. Defaults to True.")
    sourcing_model: str = Field("sow", description="The sourcing model to filter by. Defaults to 'sow'.")

@tool(args_schema=GetChecklistInput)
def get_checklists(page: int = 1, limit: int = 10, is_enabled: bool = True, sourcing_model: str = "sow") -> str:
    """ Retrieves a list of checklists from the QA environment based on the provided filters. """
    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/checklists/filter"
    
    params = {
        "page": page,
        "limit": limit,
        "is_enabled": str(is_enabled).lower(),
        "sourcing_model": sourcing_model
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
        
        # Depending on the actual response structure, you might want to process 'data'
        # For now, returning the raw JSON string as per instruction to just create the tool.
        # It is common to return specific fields if the payload is large.
        # Assuming we just want to return the relevant list.
        
        return json.dumps(data)
        
    except Exception as e:
        return f"Error fetching checklists: {str(e)}"
