import requests
from typing import Dict, Any
from langchain.tools import tool
from app.config.settings import settings
import json

@tool
def update_sow(
    program_id: str,
    sow_id: str,
    token: str,
    sow_data: Dict[str, Any]
) -> str:
    """
    Updates an existing SOW (Statement of Work) in the VMS system.
    
    Args:
        program_id: The program UUID
        sow_id: The SOW UUID to update
        token: Bearer authentication token
        sow_data: Complete SOW data dictionary containing all required fields
    
    Required fields in sow_data:
        - type: SOW type UUID
        - sow_template_id: Template UUID
        - title: SOW title
        - manager: Manager UUID
        - managed_by: Managed by UUID
        - coordinator: Coordinator UUID
        - start_date: Start date (YYYY-MM-DD)
        - end_date: End date (YYYY-MM-DD)
        - vendor: Vendor UUID
        - hierarchy_id: Hierarchy UUID
        - currency: Currency code (e.g., "INR", "USD")
        - description: HTML description
        - job_template: List of job template UUIDs
        - checklist_entity_id: Checklist entity UUID
        - checklist_version_id: Checklist version number
        - total_estimate_budget: Total budget amount
        - committed_spend: Committed spend amount (string)
        - milestone: List of milestone objects
        - standalone_deliverables: List of standalone deliverable objects
        - status: SOW status (e.g., "draft", "approved")
        
    Optional fields:
        - po_number: Purchase order number
        - external_ref_id: External reference ID
        - vendor_client_collabration: Boolean for vendor-client collaboration
        - master_data: List of master data objects
        - allow_rfx: Boolean for RFX allowance
        - rfx_id: RFX UUID (if applicable)
        - vendor_response_id: Vendor response UUID (if applicable)
        - custom_fields: List of custom field objects
        - attachments: List of attachment objects
    
    Returns:
        JSON string with the update result or error message
    """
    try:
        url = f"{settings.SOW_BASE_URL}/{program_id}/sow/{sow_id}"
        
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "origin": "https://qa-hiring.simplifysandbox.net",
            "referer": "https://qa-hiring.simplifysandbox.net/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        
        response = requests.put(url, headers=headers, json=sow_data, timeout=30)
        
        if response.status_code == 200:
            return json.dumps({
                "success": True,
                "message": "SOW updated successfully",
                "data": response.json()
            })
        else:
            return json.dumps({
                "success": False,
                "status_code": response.status_code,
                "error": response.text
            })
            
    except requests.exceptions.Timeout:
        return json.dumps({
            "success": False,
            "error": "Request timeout while updating SOW"
        })
    except requests.exceptions.RequestException as e:
        return json.dumps({
            "success": False,
            "error": f"Request failed: {str(e)}"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        })
