
import requests
import json
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetHierarchiesInput(BaseModel):
    msp_id: str = Field(..., description="The MSP ID to filter hierarchies by.")

@tool(args_schema=GetHierarchiesInput)
def get_sow_hierarchies(msp_id: str) -> str:
    """Retrieves a list of hierarchies for a specific MSP from the QA environment."""
    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/list-hierarchies"
    
    params = {
        "msp_id": msp_id
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
        return f"Error fetching hierarchies: {str(e)}"
