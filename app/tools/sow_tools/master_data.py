import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetSowMasterDataInput(BaseModel):
    master_data_type_id: str = Field(..., description="The UUID of the master data type.")
    hierarchy_ids: Optional[List[str]] = Field(None, description="Optional list of hierarchy UUIDs.")
    page: int = Field(1, description="Page number.")
    limit: int = Field(25, description="Items per page.")

@tool(args_schema=GetSowMasterDataInput)
def get_sow_master_data(master_data_type_id: str, hierarchy_ids: Optional[List[str]] = None, page: int = 1, limit: int = 25) -> str:
    """Fetches master data for a specific type in Statement Of Work (SOW)."""
    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/master-data"
    params = {"master_data_type_id": master_data_type_id}
    payload = {
        "page": page,
        "hierarchy_ids": hierarchy_ids or [],
        "limit": limit,
        "is_enabled": True,
        "sort_key": "name",
        "order_by": "asc",
        "user_id": None
    }
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'content-type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        data = response.json()
        return json.dumps(data)
    except Exception as e:
        return f"Error fetching SOW master data: {str(e)}"
