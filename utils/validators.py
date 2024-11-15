from datetime import datetime, date
import re

def validate_name(name: str) -> tuple[bool, str]:
    """Validate name input"""
    if not name:
        return False, "Name cannot be empty"
    if not re.match("^[a-zA-Z\s\-']+$", name):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    return True, ""

def validate_date(date_str: str) -> tuple[bool, str]:
    """Validate date input"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"

def validate_numeric(value: str, allow_negative: bool = False) -> tuple[bool, str]:
    """Validate numeric input"""
    try:
        num = float(value)
        if not allow_negative and num < 0:
            return False, "Value cannot be negative"
        return True, ""
    except ValueError:
        return False, "Must be a valid number"

def validate_client_id(client_id: str) -> tuple[bool, str]:
    """Validate client ID format"""
    if not client_id:
        return False, "Client ID cannot be empty"
    if not re.match("^[a-zA-Z0-9\-_]+$", client_id):
        return False, "Client ID can only contain letters, numbers, hyphens, and underscores"
    return True, "" 