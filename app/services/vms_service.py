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

    def safe_bool(val):
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.lower() == "true"
        return False

    # Rate Model Construction
    rate_model = {
        "name": "Rate Config",
        "hierarchies": [{"id": job_data.get("hierarchie_id") or job_data.get("hierarchy_id"), "name": job_data.get("hierarchy_name")}],
        "is_shift_rate": False,
        "rate_configuration": [{
            "base_rate": {
                "rate_type": {
                    "id": job_data.get("rate_type_id") or "d1b7aabd-8b02-416c-b162-162c76f327f6",
                    "name": job_data.get("rate_type_name") or "Standard Rate",
                    "abbreviation": job_data.get("rate_type_abbreviation") or "ST",
                    "rate_type_category": {
                        "id": "677ad919-65a3-4e3e-b5b3-802f68a03d9a",
                        "value": "standard",
                        "label": "Standard"
                    },
                    "is_base_rate": True,
                    "shift_type": None,
                    "min_rate": {"amount": safe_float(job_data.get("min_rate")), "is_changeable": True, "is_reduceable": False},
                    "max_rate": {"amount": safe_float(job_data.get("max_rate")), "is_changeable": True, "is_reduceable": False},
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
        "managed_by": job_data.get("managed_by") or "self-managed",
        "job_type": None,
        "job_template_id": job_data.get("job_template_id"),
<<<<<<< HEAD
        "hierarchy_ids": [job_data.get("hierarchie_id") or job_data.get("hierarchy_id")], # Corrected mapping
        "primary_hierarchy": job_data.get("primary_id") or job_data.get("hierarchie_id") or job_data.get("hierarchy_id"), # Corrected mapping
        "checklist_entity_id": job_data.get("checklist_entity_id"), # Corrected
        "checklist_version": job_data.get("checklist_version"), # Use from template/draft
        "work_location_id": job_data.get("work_location_id"), # Use from draft
        "labor_category_id": job_data.get("labour_category_id"), # Corrected spelling logic
        "work_location": {
            "id": job_data.get("work_location_id"), # Use from draft
=======
        "hierarchy_ids": [job_data.get("hierarchy_id")], # Corrected mapping
        "primary_hierarchy": job_data.get("hierarchy_id"), # Corrected mapping
        "checklist_entity_id": job_data.get("checklist_entity_id"), # Corrected
        "checklist_version": None,
        "work_location_id": None,
        "labor_category_id": job_data.get("labour_category_id"), # Corrected spelling logic
        "work_location": {
            "id": None, 
>>>>>>> 8c43841a5f9220c259199e98fc9ddc046e1669f2
            "name": job_data.get("location"), # Map location name
            "code": None, 
            "city_name": job_data.get("location"), # Use location as city fallback
            "county_name": None, 
            "zipcode": None, 
            "address_line_1": None, 
            "address_line_2": None, 
            "state_name": None
        },
<<<<<<< HEAD
        "title": job_data.get("job_title"), # Explicitly set title
        "description": job_data.get("job_description") or job_data.get("job_title"), # Fallback to title if no template desc
=======
        "description": job_data.get("job_title"), # Fallback description to Title if missing
>>>>>>> 8c43841a5f9220c259199e98fc9ddc046e1669f2
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
<<<<<<< HEAD
        "no_positions":1, # Use valid int or default 1
        "expense_allowed": "YES",
        "currency": job_data.get("currency") or "USD", # Use from draft or default USD
        "unit_of_measure": "Hourly", # Default to Hourly as unit fields were removed
        "min_bill_rate": safe_float(job_data.get("min_rate")), # Corrected key
        "max_bill_rate": safe_float(job_data.get("max_rate")), # Corrected key
        "estimated_hours_per_shift": safe_float(job_data.get("estimated_hours_per_shift")),
        "shifts_per_week": safe_float(job_data.get("shifts_per_week")),
=======
        "no_positions": safe_int(job_data.get("number_of_positions")) or 1, # Use valid int or default 1
        "expense_allowed": None,
        "currency": "USD", # Hardcoded USD as per request/default
        "unit_of_measure": "Hourly", # Default to Hourly as unit fields were removed
        "min_bill_rate": safe_float(job_data.get("min_rate")), # Corrected key
        "max_bill_rate": safe_float(job_data.get("max_rate")), # Corrected key
        "estimated_hours_per_shift": 8.0, # Defaulting to logical standard
        "shifts_per_week": 5.0, # Defaulting to logical standard
>>>>>>> 8c43841a5f9220c259199e98fc9ddc046e1669f2
        "shift": None,
        "differential_on": "",
        "differential_value": "",
        "adjustment_type": "percentage",
        "adjustment_value": 0,
        "rate_model": "bill_rate",
        "budgets": {
             # Removed complex budget calc for now to avoid errors, or keep as is if safe
            "formatted_weeks_days": "2 Weeks 4 Days",
            "working_units": "112 Hours",
            "min": {"additional_amount": "0.00000000", "single_net_budget": "11200.00000000", "net_budget": "11200.00000000", "bill_rate": str(safe_float(job_data.get("min_rate")))},
            "max": {"additional_amount": "0.00000000", "single_net_budget": "22400.00000000", "net_budget": "22400.00000000", "bill_rate": str(safe_float(job_data.get("max_rate")))},
            "avg": {"additional_amount": "0.00000000", "single_net_budget": "16800.00000000", "net_budget": "16800.00000000", "bill_rate": str(safe_float(job_data.get("max_rate")))}
        },
        "net_budget": "0.00000000",
        "expenses": [],
<<<<<<< HEAD
        "ot_exempt": safe_bool(job_data.get("ot_exempt")),
        "candidate_source": "Sourced", # Default source
=======
        "ot_exempt": False,
        "candidate_source": "Vendor", # Default source
>>>>>>> 8c43841a5f9220c259199e98fc9ddc046e1669f2
        "rates": [],
        "status": "DRAFT", # Trying OPEN instead of DRAFT if desired, or keep DRAFT
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
