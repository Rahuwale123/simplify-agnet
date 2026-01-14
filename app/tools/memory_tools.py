from langchain.tools import tool
from typing import Dict, List, Optional, Any
import json

from app.utils.context import request_session_id

# In-memory storage mimicking a database/session cache
JOB_DRAFTS = {}
SEARCH_CACHE = {} # Stores the last search result to prevent redundant API calls

def get_current_user_id():
    """Helper to get the current user ID securely from context."""
    user_id = request_session_id.get()
    return user_id if user_id else "default"

@tool
def save_field(field: str, value: Any) -> str:
    """Saves a field to the current job draft. Returns confirmation."""
    user_id = get_current_user_id()
    
    if user_id not in JOB_DRAFTS:
        JOB_DRAFTS[user_id] = {}
    
    # Normalize keys to match check_missing_fields expectations
    if field == "bill_rate_min":
        field = "min_bill_rate"
    if field == "bill_rate_max":
        field = "max_bill_rate"
        
    JOB_DRAFTS[user_id][field] = value
    return json.dumps({
        "message": f"Saved {field}",
        "current_draft": JOB_DRAFTS[user_id]
    })

@tool
def get_draft() -> dict:
    """Returns the current complete job draft."""
    user_id = get_current_user_id()
    return JOB_DRAFTS.get(user_id, {})

@tool
def get_last_search() -> dict:
    """Returns the result of the LAST search tool called (Manager, Hierarchy, etc). Use this to auto-select."""
    user_id = get_current_user_id()
    return SEARCH_CACHE.get(user_id, {})

def update_search_cache(result: dict):
    """Helper to update cache (not a tool itself)"""
    user_id = get_current_user_id()
    SEARCH_CACHE[user_id] = result

# Alias for backward compatibility with other tools
cache_tool_result = update_search_cache

def _check_missing_fields_logic() -> dict:
    """Helper function containing the logic for checking missing fields."""
    user_id = get_current_user_id()
    draft = JOB_DRAFTS.get(user_id, {})
    
    # 1. Check Job Title
    if not draft.get("job_title"):
        return {"status": "IN_PROGRESS", "missing_fields": ["job_title"], "current_draft": draft}

    # 2. Check Job Manager
    if not draft.get("job_manager_id"):
        return {"status": "IN_PROGRESS", "missing_fields": ["job_manager_id"], "current_draft": draft}
    
    # 3. Check Hierarchy
    if not draft.get("primary_hierarchy"):
        return {"status": "IN_PROGRESS", "missing_fields": ["primary_hierarchy"], "current_draft": draft}
        
    # 4. Check Job Template & Labor Category (Dependent on Hierarchy)
    if not draft.get("job_template_id"):
        return {"status": "IN_PROGRESS", "missing_fields": ["job_template_id"], "current_draft": draft}
    if not draft.get("labor_category_id"):
        # Usually selected with template, but good to check
        return {"status": "IN_PROGRESS", "missing_fields": ["labor_category_id"], "current_draft": draft}

    # 5. Check Source Type (Dependent on Hierarchy & Labor Category)
    if not draft.get("source_type"):
        return {"status": "IN_PROGRESS", "missing_fields": ["source_type"], "current_draft": draft}

    # 6. Check Date & Rates details (Requested by User)
    required_order = [
         "start_date",
         "end_date",
         "positions",
         "currency",
         "unit", # Corrected from unit_of_measure via user finding
         "hours_per_day", # Corrected
         "days_per_week", # Corrected
         "min_bill_rate", 
         "max_bill_rate" 
    ]
    
    missing = [f for f in required_order if f not in draft]

    if missing:
        return {"status": "IN_PROGRESS", "missing_fields": missing, "current_draft": draft}

    return {"status": "ReADy", "missing_fields": [], "current_draft": draft}

@tool
def check_missing_fields() -> dict:
    """
    Checks the current draft against required fields. 
    Returns a dict with keys: 'status' (IN_PROGRESS or ReADy), 'missing_fields' (list), and 'current_draft' (dict).
    """
    return _check_missing_fields_logic()

@tool
def submit_job() -> str:
    """
    FINAL STEP TOOL.
    Call this ONLY when `check_missing_fields` returns 'ReADy'.
    It generates the required JSON signal for the UI to show completion buttons.
    """
    # Double check internally
    check = _check_missing_fields_logic()
    if check['missing_fields']:
        return f"Error: Cannot submit. Missing items: {check['missing_fields']}"
    
    # Construct the Final UI JSON
    # The agent will repeat this in the Final Answer
    return json.dumps({
       "ui_action": "show_completion_buttons",
       "create_job_now": True,
       "draft_data": check['current_draft']
    })
