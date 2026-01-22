import requests
from typing import Dict, Any, Optional
import os
from app.config.settings import settings


class SimplifySOWTool:
    """
    Tool to create SOW (Statement of Work) in Simplify system
    """

    BASE_URL = os.getenv("API_BASE_URL") 

    def __init__(self, bearer_token: str):
        if not bearer_token:
            raise ValueError("Bearer token is required")

        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def create_sow(
        self,
        program_id: str,
        sow_type: str,
        hierarchy_id: str,
        manager: str,
        coordinator: str,
        sow_template_id: str,
        title: str,
        start_date: str,
        end_date: str,
        currency: str,
        vendor: str,
        committed_spend: float,
        description: Optional[str] = None,
        status: str = "draft",
        extra_payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create SOW in Simplify system
        """

        if not program_id:
            raise ValueError("program_id is mandatory")

        url = f"{self.BASE_URL}/sow/v1/api/program/{program_id}/sow"

        payload = {
            "type": sow_type,
            "hierarchy_id": hierarchy_id,
            "manager": manager,
            "coordinator": coordinator,
            "sow_template_id": sow_template_id,
            "title": title,
            "start_date": start_date,
            "end_date": end_date,
            "currency": currency,
            "vendor": vendor,
            "committed_spend": committed_spend,
            "status": status
        }

        if description:
            payload["description"] = description

        if extra_payload:
            payload.update(extra_payload)

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        try:
            response_data = response.json()
        except Exception:
            response_data = response.text

        return {
            "success": response.status_code in (200, 201),
            "status_code": response.status_code,
            "response": response_data
        }
