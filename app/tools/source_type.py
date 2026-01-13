import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings
from app.tools.memory_tools import cache_tool_result

class GetSourceTypesInput(BaseModel):
    hierarchy_ids: List[str] = Field(..., description="List of hierarchy UUIDs.")
    labor_category_ids: List[str] = Field(..., description="List of labor category UUIDs.")

@tool(args_schema=GetSourceTypesInput)
def get_source_types(hierarchy_ids: List[str], labor_category_ids: List[str]) -> str:
    """Retrieves the list of available source types (e.g. Sourced, Payrolled) for given hierarchies and labor categories."""
    token = request_token.get()
    program_id = request_program_id.get()

    # Base URL from settings + program_id + specific path
    # Endpoint: /vendor/source-type
    url = f"{settings.API_BASE_URL}/{program_id}/vendor/source-type"
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'content-type': 'application/json',
        'origin': 'https://qa-hiring.simplifysandbox.net',
        'referer': 'https://qa-hiring.simplifysandbox.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }

    payload = {
        "hierarchies": hierarchy_ids,
        "labor_category": labor_category_ids
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # User requested to parse out the 'data' array only
        source_types = data.get("data", [])
        if not source_types:
            return "No source types found."

        # CACHE THE RESULT
        cache_tool_result(source_types)

        return json.dumps({"source_types": source_types})
    except Exception as e:
        return f"Error fetching source types: {str(e)}"
