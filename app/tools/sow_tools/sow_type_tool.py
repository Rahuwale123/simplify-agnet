
import requests
import json
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token
from app.config.settings import settings

class GetSowTypesInput(BaseModel):
    # No input needed as specifically asked for SOW Type which implies fixed slug,
    # but good practice to allow overriding or just keeping it empty.
    # The user said "Field - mandatory", which might refer to the output selection? 
    # Or maybe the slug? The curl shows slug=sow_type.
    # I'll stick to no required input for the tool usage itself to be simple.
    pass

@tool(args_schema=GetSowTypesInput)
def get_sow_types() -> str:
    """Retrieves the list of SOW Types from the QA environment."""
    token = request_token.get()
    
    # URL from the curl request
    url = "https://v4-qa.simplifysandbox.net/config/v1/api/get-all/pickList"
    params = {
        "slug": "sow_type"
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
        
        # Returning raw json as requested for tool creation phase
        return json.dumps(data)
        
    except Exception as e:
        return f"Error fetching SOW types: {str(e)}"
