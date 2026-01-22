import requests
import json
from typing import Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetRateConfigurationsInput(BaseModel):
    hierarchy_id: str = Field(..., description="The UUID of the hierarchy.")
    job_template_id: str = Field(..., description="The UUID of the job template.")
    labour_category_id: str = Field(..., description="The UUID of the labor category.")
    work_location_id: str = Field(..., description="The UUID of the work location.")
    currency_id: str = Field("USD", description="The currency ID (e.g., USD, ZAR).")
    unit_of_measure: str = Field("Hourly", description="The unit of measure (e.g., Hourly).")

@tool(args_schema=GetRateConfigurationsInput)
def get_rate_configurations(
    hierarchy_id: str,
    job_template_id: str,
    labour_category_id: str,
    work_location_id: str,
    currency_id: str = "USD",
    unit_of_measure: str = "Hourly"
) -> str:
    """Retrieves rate configurations (min/max rates) based on hierarchy, template, labor category, and location."""
    token = request_token.get()
    program_id = request_program_id.get()

    # The settings.API_BASE_URL likely ends with /program, so we append the configurations path
    url = f"{settings.API_BASE_URL}/{program_id}/rate-configurations"
    
    params = {
        "hierarchie_id": hierarchy_id, # Note the specific spelling from the provided cURL
        "job_templates": job_template_id,
        "unit_of_measure": unit_of_measure,
        "currency_id": currency_id,
        "labor_category_id": labour_category_id,
        "is_shift_rate": 0,
        "work_location_id": work_location_id
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'cache-control': 'no-cache',
        'origin': 'https://qa-hiring.simplifysandbox.net',
        'referer': 'https://qa-hiring.simplifysandbox.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract min/max rate based on the provided nested structure
        # Path: rate_configurations[0].rate_configuration[0].base_rate.rate_type.min_rate/max_rate
        rate_configs = data.get("rate_configurations", [])
        if not rate_configs:
            return json.dumps({"error": "No rate configurations found", "raw": data})
            
        first_config = rate_configs[0]
        rc_list = first_config.get("rate_configuration", [])
        if not rc_list:
            return json.dumps({"error": "No rate_configuration list found", "raw": data})
            
        base_rate = rc_list[0].get("base_rate", {})
        rate_type = base_rate.get("rate_type", {})
        
        min_rate_obj = rate_type.get("min_rate", {})
        max_rate_obj = rate_type.get("max_rate", {})
        
        min_amount = min_rate_obj.get("amount")
        max_amount = max_rate_obj.get("amount")
        
        if min_amount is None or max_amount is None:
             return json.dumps({"error": "Rates not found in nested structure", "raw": data})

        return json.dumps({
            "min_rate": min_amount,
            "max_rate": max_amount,
            "rate_type_id": rate_type.get("id"),
            "rate_type_name": rate_type.get("name"),
            "rate_type_abbreviation": rate_type.get("abbreviation")
        })
    except Exception as e:
        return f"Error fetching rate configurations: {str(e)}"
