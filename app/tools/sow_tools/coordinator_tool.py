
import requests
import json
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetCoordinatorsInput(BaseModel):
    hierarchy_id: str = Field(..., description="The Hierarchy ID to filter coordinators by. This is a mandatory field.")
    page: int = Field(1, description="Page number for pagination.")
    size: int = Field(10, description="Number of items per page.")

@tool(args_schema=GetCoordinatorsInput)
def get_sow_coordinators(hierarchy_id: str, page: int = 1, size: int = 10) -> str:
    """Retrieves a list of coordinators (MSP managers) for a specific hierarchy from the QA environment."""
    token = request_token.get()
    program_id = request_program_id.get()

    # Note: Using the same endpoint as job managers but with is_msp=true
    url = f"{settings.API_BASE_URL}/{program_id}/get-job-manegers"
    
    params = {
        "page": page,
        "size": size,
        "hierarchy_id": hierarchy_id,
        "is_msp": "true"
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
        return f"Error fetching coordinators: {str(e)}"
