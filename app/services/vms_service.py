import requests
import json
from app.config.settings import settings

def create_job_vms(program_id: str, token: str, job_data: dict):
    """
    Creates a job in the VMS system using the provided job_data (draft).
    Constructs the complex payload expected by the VMS API.
    """
    # Using API_BASE_URL from settings to match other tools (config/v1) or sourcing/v1 if distinct
    # Attempting to align with the working tools first.
    # If API_BASE_URL is .../config/v1/api/program, then this becomes .../config/v1/api/program/{id}/job
    # However, standard might be Sourcing. Let's try to trust the Settings first if "sourcing" failed.
    # url = f"https://v4-qa.simplifysandbox.net/sourcing/v1/api/program/{program_id}/job"
    
    # Actually, let's keep the domain but switch service if needed.
    # But for now, let's assume the user provided token is good for the base URL used elsewhere.
    # Using the exact URL provided by the user which aligns with the sourcing service
    url = f"https://v4-qa.simplifysandbox.net/sourcing/v1/api/program/{program_id}/job"
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'authorization': f'Bearer {token}' if token and not token.startswith('Bearer') else token,
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://qa-hiring.simplifysandbox.net',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://qa-hiring.simplifysandbox.net/',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    }

    # Helper to safe convert to float/int
    def safe_float(val):
        try:
            return float(val) if val else 0.0
        except ValueError:
            return 0.0
            
    def safe_int(val):
        try:
            return int(val) if val else 0
        except ValueError:
            return 0

    # Rate Model Construction
    rate_model = {
        "name": "Rate Config for Standard ",
        "hierarchies": [{"id": job_data.get("primary_hierarchy"), "name": "AI VMS Program"}], # Name is hardcoded/assumed or needs fetch
        "is_shift_rate": False,
        "rate_configuration": [{
            "base_rate": {
                "rate_type": {
                    "id": "d1b7aabd-8b02-416c-b162-162c76f327f6", # Hardcoded standard rate ID
                    "name": "Standard Rate",
                    "abbreviation": "ST",
                    "rate_type_category": {
                        "id": "677ad919-65a3-4e3e-b5b3-802f68a03d9a",
                        "value": "standard",
                        "label": "Standard"
                    },
                    "is_base_rate": True,
                    "shift_type": None,
                    "min_rate": {"amount": safe_float(job_data.get("min_bill_rate") or job_data.get("bill_rate_min")), "is_changeable": True, "is_reduceable": False},
                    "max_rate": {"amount": safe_float(job_data.get("max_bill_rate") or job_data.get("bill_rate_max")), "is_changeable": True, "is_reduceable": False},
                    "min_max_rate": {"max_rate": "0.00000000", "min_rate": "0.00000000"},
                    "is_enabled": True
                },
                "seq_number": 0,
                "rates": []
            }
        }]
    }

    # Date formatting
    start_date = f"{job_data.get('start_date')}T00:00:00.000Z" if job_data.get('start_date') else None
    end_date = f"{job_data.get('end_date')}T00:00:00.000Z" if job_data.get('end_date') else None

    # Full Payload
    payload = {
        "job_manager_id": job_data.get("job_manager_id"),
        "managed_by": "self-managed",
        "job_type": None,
        "job_template_id": job_data.get("job_template_id"),
        "hierarchy_ids": [job_data.get("primary_hierarchy")],
        "primary_hierarchy": job_data.get("primary_hierarchy"),
        "checklist_entity_id": None,
        "checklist_version": None,
        "work_location_id": None,
        "labor_category_id": job_data.get("labor_category_id"),
        "work_location": {
            "id": None, "name": None, "code": None, "city_name": None, 
            "county_name": None, "zipcode": None, "address_line_1": None, 
            "address_line_2": None, "state_name": None
        },
        "description": None,
        "additional_attachments": [],
        "qualifications": [],
        "description_url": None,
        "allow_per_identified_s": False,
        "candidates": [],
        "foundationDataTypes": None,
        "custom_fields": [],
        "rate": [rate_model],
        "is_shift_type": False,
        "start_date": start_date,
        "end_date": end_date,
        "no_positions": safe_int(job_data.get("positions")),
        "expense_allowed": None,
        "currency": job_data.get("currency"),
        "unit_of_measure": job_data.get("unit"),
        "min_bill_rate": safe_float(job_data.get("min_bill_rate") or job_data.get("bill_rate_min")),
        "max_bill_rate": safe_float(job_data.get("max_bill_rate") or job_data.get("bill_rate_max")),
        "estimated_hours_per_shift": safe_float(job_data.get("hours_per_day")),
        "shifts_per_week": safe_float(job_data.get("days_per_week")),
        "shift": None,
        "differential_on": "",
        "differential_value": "",
        "adjustment_type": "percentage",
        "adjustment_value": 0,
        "rate_model": "bill_rate",
        "budgets": {
            "formatted_weeks_days": "2 Weeks 4 Days",
            "working_units": "112 Hours",
            "min": {"additional_amount": "0.00000000", "single_net_budget": "11200.00000000", "net_budget": "11200.00000000", "bill_rate": "100.00000000"},
            "max": {"additional_amount": "0.00000000", "single_net_budget": "22400.00000000", "net_budget": "22400.00000000", "bill_rate": "200.00000000"},
            "avg": {"additional_amount": "0.00000000", "single_net_budget": "16800.00000000", "net_budget": "16800.00000000", "bill_rate": "150.00000000"}
        },
        "net_budget": "$16800.00000000",
        "expenses": [],
        "ot_exempt": False,
        "candidate_source": job_data.get("source_type"),
        "rates": [],
        "status": "OPEN",
        "source": "TEMPLATE",
        "event_slug": "create_job",
        "module_id": "",
        "sourcing_model": "contingent"
    }

    print(f"Submitting Job Payload to VMS: {json.dumps(payload, indent=2)}")
    print(f"Using Token (first 50 chars): {token[:50]}...")

    response = requests.post(url, headers=headers, json=payload)
    if not response.ok:
        print(f"VMS Error: {response.text}")
    response.raise_for_status()
    
    return response.json()
