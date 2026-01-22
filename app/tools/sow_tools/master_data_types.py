import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetSowMasterDataTypesInput(BaseModel):
    hierarchy_ids: Optional[List[str]] = Field(None, description="List of hierarchy UUIDs to filter master data types.")
    page: int = Field(1, description="Page number.")
    limit: int = Field(100, description="Items per page.")

@tool(args_schema=GetSowMasterDataTypesInput)
def get_sow_master_data_types(hierarchy_ids: Optional[List[str]] = None, page: int = 1, limit: int = 100) -> str:
    """Fetches master data types for Statement Of Work (SOW)."""
    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/master-data-types"
    payload = {
        "page": page,
        "hierarchy_ids": hierarchy_ids or [],
        "limit": limit,
        "is_enabled": True,
        "order_by_seq_number": True,
        "allow_multiple_sows": True
    }
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'content-type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return json.dumps(data)
    except Exception as e:
        return f"Error fetching SOW master data types: {str(e)}"
