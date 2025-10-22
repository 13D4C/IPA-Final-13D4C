import os
import json
import requests
from dotenv import load_dotenv

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings()

load_dotenv()

# --- Constants ---
ROUTER_HOST = os.environ.get("ROUTER_HOST")
ROUTER_USER = os.environ.get("ROUTER_USER", "admin")
ROUTER_PASS = os.environ.get("ROUTER_PASS", "cisco")
STUDENT_ID = "66070216"
INTERFACE_NAME = f"Loopback{STUDENT_ID}"

BASE_API_URL = f"https://{ROUTER_HOST}/restconf/data/ietf-interfaces:interfaces"
INTERFACE_URL = f"{BASE_API_URL}/interface={INTERFACE_NAME}"
STATE_URL = f"https://{ROUTER_HOST}/restconf/data/ietf-interfaces:interfaces-state/interface={INTERFACE_NAME}"

HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
AUTH = (ROUTER_USER, ROUTER_PASS)

# --- Helper Function ---
def _check_interface_exists():
    """Checks if the loopback interface already exists."""
    try:
        response = requests.get(INTERFACE_URL, auth=AUTH, headers=HEADERS, verify=False)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error checking interface existence: {e}")
        return False

# --- Core Functions (Updated Response Format) ---
def create_interface():
    """Creates a new loopback interface."""
    if _check_interface_exists():
        return f"Cannot create: Interface loopback {STUDENT_ID}"

    payload = {
        "ietf-interfaces:interface": {
            "name": INTERFACE_NAME,
            "description": f"{STUDENT_ID} Loopback interface",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [{"ip": "172.2.16.1", "netmask": "255.255.255.0"}]
            }
        }
    }
    try:
        response = requests.put(INTERFACE_URL, data=json.dumps(payload), auth=AUTH, headers=HEADERS, verify=False)
        if response.status_code == 201:
            return f"Interface loopback {STUDENT_ID} is created successfully"
        else:
            return f"Cannot create: Interface loopback {STUDENT_ID}"
    except requests.exceptions.RequestException:
        return f"Cannot create: Interface loopback {STUDENT_ID}"

def delete_interface():
    """Deletes the loopback interface."""
    if not _check_interface_exists():
        return f"Cannot delete: Interface loopback {STUDENT_ID}"
        
    try:
        response = requests.delete(INTERFACE_URL, auth=AUTH, headers=HEADERS, verify=False)
        if response.status_code == 204:
            return f"Interface loopback {STUDENT_ID} is deleted successfully"
        else:
            return f"Cannot delete: Interface loopback {STUDENT_ID}"
    except requests.exceptions.RequestException:
        return f"Cannot delete: Interface loopback {STUDENT_ID}"

def _set_interface_state(is_enabled: bool):
    """Helper function to enable or disable the interface."""
    action = "enable" if is_enabled else "shutdown"
    success_action = "enabled" if is_enabled else "shutdowned"
    
    if not _check_interface_exists():
        return f"Cannot {action}: Interface loopback {STUDENT_ID}"
        
    payload = {
        "ietf-interfaces:interface": {
            "name": INTERFACE_NAME,
            "enabled": is_enabled
        }
    }
    try:
        # Using PATCH is more efficient for modifying existing data
        response = requests.patch(INTERFACE_URL, data=json.dumps(payload), auth=AUTH, headers=HEADERS, verify=False)
        if response.status_code == 204:
            return f"Interface loopback {STUDENT_ID} is {success_action} successfully"
        else:
            return f"Cannot {action}: Interface loopback {STUDENT_ID}"
    except requests.exceptions.RequestException:
        return f"Cannot {action}: Interface loopback {STUDENT_ID}"

def enable_interface():
    """Enables the loopback interface."""
    return _set_interface_state(True)

def disable_interface():
    """Disables (shutdowns) the loopback interface."""
    return _set_interface_state(False)

def get_interface_status():
    """Retrieves the simplified admin and operational status of the interface."""
    try:
        response = requests.get(STATE_URL, auth=AUTH, headers=HEADERS, verify=False)
        if response.status_code == 200:
            data = response.json().get("ietf-interfaces:interface", {})
            admin_status = data.get("admin-status", "unknown")
            if admin_status == 'up':
                return f"Interface loopback {STUDENT_ID} is enabled"
            else:
                return f"Interface loopback {STUDENT_ID} is disabled"
        elif response.status_code == 404:
            return f"No Interface loopback {STUDENT_ID}"
        else:
            return f"Error getting status for loopback {STUDENT_ID}"
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        return f"Error getting status for loopback {STUDENT_ID}"