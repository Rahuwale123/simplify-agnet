import requests
from typing import List
from langchain.tools import tool
from app.config.settings import settings
import json

@tool
def approve_sow(
    program_id: str,
    sow_id: str,
    token: str,
    rejected_milestone_ids: List[str] = None,
    is_updated: int = 0
) -> str:
    """
    Approves an existing SOW (Statement of Work) in the VMS system.
    
    Args:
        program_id: The program UUID
        sow_id: The SOW UUID to approve
        token: Bearer authentication token
        rejected_milestone_ids: List of milestone IDs to reject (default: empty list)
        is_updated: Flag indicating if SOW was updated (0 or 1, default: 0)
    
    Returns:
        JSON string with the approval result or error message
    """
    try:
        url = f"{settings.SOW_BASE_URL}/{program_id}/sow/{sow_id}/approval"
        
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "origin": "https://qa-hiring.simplifysandbox.net",
            "referer": "https://qa-hiring.simplifysandbox.net/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        
        payload = {
            "rejected_milestone_ids": rejected_milestone_ids if rejected_milestone_ids else [],
            "is_updated": is_updated
        }
        
        response = requests.put(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return json.dumps({
                "success": True,
                "message": "SOW approved successfully",
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
            "error": "Request timeout while approving SOW"
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
