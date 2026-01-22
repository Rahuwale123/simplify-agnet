import requests
import json
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings
from typing import Optional

class FetchMSPInput(BaseModel):
    hierarchy_id: str = Field(..., description="The UUID of the hierarchy to fetch MSP for.")

@tool(args_schema=FetchMSPInput)
def fetch_msp(hierarchy_id: str) -> str:
    """Fetches the MSP (Managed Service Provider) for a specific hierarchy. Use this to determine the 'managed_by' value."""
    token = request_token.get()
    program_id = request_program_id.get()

    # URL provided by user
    url = f"{settings.API_BASE_URL}/{program_id}/fetch-msp"
    params = {"hierarchy_id": hierarchy_id}
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        msp_list = data.get("data", [])
        if not msp_list:
            return "No MSP found for this hierarchy."

        # The user wants the name/display_name for 'managed_by'
        msp = msp_list[0]
        return json.dumps({
            "msp_name": msp.get("display_name") or msp.get("name"),
            "msp_id": msp.get("id"),
            "message": "MSP fetched successfully"
        })
    except Exception as e:
        return f"Error fetching MSP: {str(e)}"
