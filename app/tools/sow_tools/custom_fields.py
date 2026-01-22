import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetSowCustomFieldsInput(BaseModel):
    hierarchy_ids: Optional[List[str]] = Field(None, description="Optional list of hierarchy UUIDs.")
    page: int = Field(1, description="Page number.")
    limit: int = Field(100, description="Items per page.")

@tool(args_schema=GetSowCustomFieldsInput)
def get_sow_custom_fields(hierarchy_ids: Optional[List[str]] = None, page: int = 1, limit: int = 100) -> str:
    """Fetches custom fields for the Statement Of Work (SOW) module."""
    token = request_token.get()
    program_id = request_program_id.get()

    # Join hierarchy IDs for query string
    h_ids_str = ",".join(hierarchy_ids) if hierarchy_ids else ""
    
    url = f"{settings.API_BASE_URL}/{program_id}/custom-fields"
    params = {
        "module_name": "Statement Of Work",
        "info_level": "detail",
        "is_enabled": "true",
        "limit": limit,
        "page": page,
        "hierarchy_ids": h_ids_str
    }
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return json.dumps(data)
    except Exception as e:
        return f"Error fetching SOW custom fields: {str(e)}"
