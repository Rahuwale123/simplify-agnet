from typing import Dict, Any, List
from langchain.tools import tool
import json

# Schema definition for fields required to create a job/filter managers
job_manager_filter_schema = {
    "job_manager_id": "",
    "hierarchy_id": "",
    "labour_category_id": "",
    "checklist_entity_id": "",
    "job_template_id": "",
    "start_date": "",
    "end_date": "",
    "min_rate": "",
    "max_rate": "",
    "number_of_positions": "",
}

# Global in-memory storage for the draft (Temporary solution, should use DB/Redis)
job_manager_filter_data: Dict[str, Any] = {}

def find_missing_fields(input_data: dict, schema: dict) -> list:
    missing = []

    # Updated to allow None values as per user request (for optional IDs from templates)
    for field in schema.keys():
        if field not in input_data:
            missing.append(field)
        else:
            value = input_data[field]
            # Only flag as missing if it's an empty STRING. Allow None/Objects.
            if isinstance(value, str) and value.strip() == "":
                missing.append(field)

    return missing

@tool
def save_field(field_name: str, value: Any) -> str:
    """Saves a field value to the job draft. Returns the updated draft status."""
    if not field_name:
        return "Error: Field name is required"

    # Only error on empty strings. Allow None.
    if isinstance(value, str) and value.strip() == "":
        return f"Error: Empty value for field: {field_name}"

    job_manager_filter_data[field_name] = value
    
    # Check what's still missing
    missing = find_missing_fields(job_manager_filter_data, job_manager_filter_schema)
    if missing:
        return f"Saved {field_name}. Remaining missing fields: {', '.join(missing)}"
    else:
        return f"Saved {field_name}. All fields present. Ready to submit."

def save_job_draft(user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Saves the entire job draft for a user. Currently uses the global dict."""
    # In a real app, this should be keyed by user_id
    global job_manager_filter_data
    if data is None:
        data = {}
    
    # Overwrite the global data with new data (or clear it)
    job_manager_filter_data.clear()
    job_manager_filter_data.update(data)
    
    return job_manager_filter_data

def get_job_draft(user_id: str) -> Dict[str, Any]:
    """Retrieves the job draft for a user."""
    # Currently ignoring user_id as per the simple global impl above
    return job_manager_filter_data

@tool
def get_draft(query: str = "") -> str:
    """Returns the current job draft values."""
    return json.dumps(job_manager_filter_data)

@tool
def check_missing_fields(query: str = "") -> str:
    """Checks which fields are still missing from the job draft."""
    missing = find_missing_fields(job_manager_filter_data, job_manager_filter_schema)
    if missing:
        return f"Missing fields: {', '.join(missing)}"
    else:
        return "All required fields are present."

