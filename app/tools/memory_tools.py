from typing import Optional, Any, Dict
from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
import json
from app.utils.context import request_session_id

# Global store for job drafts, keyed by session_id/user_id
JOB_DRAFTS = {}
# Global store for the last tool output to prevent ID hallucinations
SEARCH_CACHE = {}

def get_current_draft():
    session_id = request_session_id.get() or "default"
    if session_id not in JOB_DRAFTS:
        JOB_DRAFTS[session_id] = {}
    return JOB_DRAFTS[session_id]

def cache_tool_result(result_key: str, data: Any):
    """Helper for other tools to cache their results."""
    session_id = request_session_id.get() or "default"
    if session_id not in SEARCH_CACHE:
        SEARCH_CACHE[session_id] = {}
    SEARCH_CACHE[session_id] = {"key": result_key, "data": data}

class SaveFieldInput(BaseModel):
    field: str = Field(..., description="The field name to save (e.g., 'job_title', 'job_manager_id').")
    value: Any = Field(..., description="The value to save.")

@tool(args_schema=SaveFieldInput)
def save_field(field: str, value: Any) -> str:
    """Saves a field to the in-memory job draft dictionary."""
    draft = get_current_draft()
    draft[field] = value
    return json.dumps({"message": f"Saved {field}", "current_draft": draft})

@tool
def get_draft() -> str:
    """Retrieves the current job draft from memory."""
    draft = get_current_draft()
    return json.dumps(draft)

@tool
def get_last_search() -> str:
    """Retrieves the result of the LAST search tool called (e.g. managers, hierarchies).
    Use this when the user says 'Yes' to find the ID you just discovered.
    """
    session_id = request_session_id.get() or "default"
    result = SEARCH_CACHE.get(session_id, {})
    return json.dumps(result)

@tool
def check_missing_fields() -> str:
    """Checks what fields are missing from the workflow."""
    draft = get_current_draft()
    required_order = [
        "job_title", 
        "job_manager_id", 
        "primary_hierarchy", 
        "job_template_id", 
        "source_type",
        "labor_category_id",
        "start_date",
        "end_date",
        "positions",
        "currency",
        "unit",
        "hours_per_day",
        "days_per_week",
        "bill_rate_min",
        "bill_rate_max" 
    ]
    
    missing = [f for f in required_order if f not in draft]
    return json.dumps({
        "status": "IN_PROGRESS" if missing else "ReADy",
        "missing_fields": missing,
        "current_draft": draft
    })
