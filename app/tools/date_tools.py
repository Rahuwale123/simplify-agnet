from langchain.tools import tool
import datetime
from typing import Optional
import json

@tool
def get_current_date() -> str:
    """Returns the current date in YYYY-MM-DD format. Use this to auto-calculate years for user-provided dates."""
    today = datetime.datetime.now()
    return json.dumps({"current_date": today.strftime("%Y-%m-%d"), "year": today.year})

@tool
def resolve_date(date_str: str, current_year: int) -> str:
    """
    Intelligently resolves a Date string (e.g., '12 jan') to 'YYYY-MM-DD'.
    - If year is missing, uses current_year.
    - If user provides start and end date, end date CANNOT be before start date.
    - This tool returns a formatted date string.
    """
    # Basic date parsing logic for common relative terms
    date_str = date_str.lower().strip()
    today = datetime.datetime.now()
    resolved = None
    
    import re

    # 1. Keywords
    if date_str in ["today", "now"]:
        resolved = today
    elif date_str == "tomorrow":
        resolved = today + datetime.timedelta(days=1)
    elif date_str == "yesterday":
        resolved = today - datetime.timedelta(days=1)
    elif "day after tomorrow" in date_str:
        resolved = today + datetime.timedelta(days=2)
    elif "next week" in date_str:
        resolved = today + datetime.timedelta(weeks=1)
    
    # 2. "Day Month" (e.g. "17 march", "17 mar")
    elif re.match(r"^\d{1,2}\s+[a-z]+$", date_str):
        try:
            day, month_str = date_str.split()
            # Parse fake date to get month number
            dt = datetime.datetime.strptime(f"{day} {month_str} {current_year}", "%d %B %Y")
            resolved = dt
        except:
             try: # Try short month name
                dt = datetime.datetime.strptime(f"{day} {month_str} {current_year}", "%d %b %Y")
                resolved = dt
             except: pass

    # 3. "Month Day" (e.g. "march 17")
    elif re.match(r"^[a-z]+\s+\d{1,2}$", date_str):
        try:
            month_str, day = date_str.split()
            dt = datetime.datetime.strptime(f"{day} {month_str} {current_year}", "%d %B %Y")
            resolved = dt
        except: pass

    # 4. "N months from..."
    # Very basic: if "2 months", add 60 days
    match_months = re.search(r"(\d+)\s+month", date_str)
    if not resolved and match_months:
        months = int(match_months.group(1))
        # Base it on today or tomorrow? User said "2 month from tomorrow"
        base = today + datetime.timedelta(days=1) if "tomorrow" in date_str else today
        # Approx 30 days per month
        resolved = base + datetime.timedelta(days=months*30)

    if not resolved:
        return f"Could not auto-resolve '{date_str}'. Please use format YYYY-MM-DD."

    return json.dumps({
        "original": date_str,
        "resolved_date": resolved.strftime("%Y-%m-%d"),
        "year": resolved.year
    })
