import requests
import json
from typing import List, Optional
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from app.utils.context import request_token, request_program_id
from app.config.settings import settings

class GetJobTemplatesInput(BaseModel):
    hierarchy_id: str = Field(..., description="The UUID of the hierarchy to filter job templates.")
    is_enabled: bool = Field(True, description="Filter for enabled templates.")

@tool(args_schema=GetJobTemplatesInput)
def get_job_templates(hierarchy_id: str, is_enabled: bool = True) -> str:
    """Retrieves the list of job templates for a specific hierarchy from the QA environment."""
    token = request_token.get()
    program_id = request_program_id.get()

    url = f"{settings.API_BASE_URL}/{program_id}/job-templates"
    params = {
        "hierarchy": hierarchy_id,
        "is_enabled": str(is_enabled).lower()
    }
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'origin': 'https://qa-hiring.simplifysandbox.net',
        'referer': 'https://qa-hiring.simplifysandbox.net/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        job_templates = data.get("job_templates", [])
        if not job_templates:
            return "No job templates found."

        result = []
        for t in job_templates:
            # Extract specific fields as requested: 
            # template name, template id, labour category id, primary hierarchy
            template_name = t.get("template_name")
            template_id = t.get("id")
            labour_category_id = t.get("labour_category_id")
            primary_hierarchy = t.get("primary_hierarchy", {})
            checklist_entity_id = t.get("checklist_entity_id") # Keep this for future saves

            result.append({
                "template_name": template_name,
                "template_id": template_id,
                "labour_category_id": labour_category_id,
                "primary_hierarchy": primary_hierarchy,
                "checklist_entity_id": checklist_entity_id,
                # Additional fields for Phase 5 Auto-fill
                "estimated_hours_per_shift": t.get("estimated_hours_per_shift"),
                "shifts_per_week": t.get("shifts_per_week"),
                "description": t.get("description"),
                "min_bill_rate": t.get("min_bill_rate"),
                "max_bill_rate": t.get("max_bill_rate")
            })

        # CACHE THE RESULT
        # cache result removal

        return json.dumps({"templates": result})
    except Exception as e:
        return f"Error fetching job templates: {str(e)}"
