from typing import Dict, Any, List
from langchain.tools import tool
import json

# Schema definition for fields required to create a job/filter managers
job_manager_filter_schema = {
    "job_manager_id": "", 
    "hierarchy_id": "",  # Get default hierarchy id from job manager via api
    "labour_category_id": "", # Job template
    "checklist_entity_id": "", # Job template
    "job_template_id": "", # From job title (find template id by title if not found create one)
    "start_date": "",
    "end_date": "",
    "min_rate": "", # From rate card
    "max_rate": "", # From rate card
    "number_of_positions": "1", # Hard code to 1
    "currency": "",
    "location": "", # Location name
    "work_location_id": "",
    "job_description": "", # From job template
    "checklist_version": "", # From job template
    "hierarchy_name": "", # From hierarchy tool
    "ot_exempt": "", # True/False based on classification
    "estimated_hours_per_shift": "", # From job template
    "shifts_per_week": "", # From job template
    "rate_type_id": "", # From rate configuration tool
    "rate_type_name": "", # From rate configuration tool
    "rate_type_abbreviation": "", # From rate configuration tool
}

from app.services.redis_service import redis_service
from app.utils.context import request_session_id

# Global schema definition remains
job_manager_filter_schema = {
    "job_manager_id": "", 
    "hierarchie_id": "", 
    "primary_id": "",
    "managed_by": "",
    "labour_category_id": "", 
    "checklist_entity_id": "", 
    "job_template_id": "", 
    "start_date": "",
    "end_date": "",
    "min_rate": "", 
    "max_rate": "", 
    "currency": "",
    "location": "", 
    "work_location_id": "",
    "job_description": "", 
    "checklist_version": "", 
    "hierarchy_name": "", 
    "ot_exempt": "", 
    "estimated_hours_per_shift": "", 
    "shifts_per_week": "", 
    "rate_type_id": "", 
    "rate_type_name": "", 
    "rate_type_abbreviation": "", 
}

def find_missing_fields(input_data: dict, schema: dict) -> list:
    missing = []
    for field in schema.keys():
        if field not in input_data:
            missing.append(field)
        else:
            value = input_data[field]
            if isinstance(value, str) and value.strip() == "":
                missing.append(field)
    return missing

@tool
def save_field(field_name: str, value: Any) -> str:
    """Saves a field value to the job draft. Returns the updated draft status."""
    session_id = request_session_id.get() or "default"
    if not field_name:
        return "Error: Field name is required"

    if isinstance(value, str) and value.strip() == "":
        return f"Error: Empty value for field: {field_name}"

    draft = redis_service.get_draft(session_id)
    draft[field_name] = value
    redis_service.save_draft(session_id, draft)
    
    missing = find_missing_fields(draft, job_manager_filter_schema)
    if missing:
        return f"Saved {field_name}. Remaining missing fields: {', '.join(missing)}"
    else:
        return f"Saved {field_name}. All fields present. Ready to submit."

def save_job_draft(session_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Saves the entire job draft for a session."""
    # This overwrite behavior is used by reset
    redis_service.save_draft(session_id, data or {})
    return data

def get_job_draft(session_id: str) -> Dict[str, Any]:
    """Retrieves the job draft for a session."""
    return redis_service.get_draft(session_id)

@tool
def get_draft(query: str = "") -> str:
    """Returns the current job draft values."""
    session_id = request_session_id.get() or "default"
    draft = redis_service.get_draft(session_id)
    return json.dumps(draft)

@tool
def check_missing_fields(query: str = "") -> str:
    """Checks which fields are still missing from the job draft."""
    session_id = request_session_id.get() or "default"
    draft = redis_service.get_draft(session_id)
    missing = find_missing_fields(draft, job_manager_filter_schema)
    if missing:
        return f"Missing fields: {', '.join(missing)}"
    else:
        return "All required fields are present."

