import json
import requests
requests.packages.urllib3.disable_warnings()

# --- ข้อมูลเฉพาะของคุณ ---
STUDENT_ID = "66070216"
ROUTER_IP = "10.0.15.62"
# -------------------------

last_three = int(STUDENT_ID[-3:])
x = last_three // 100
y = last_three % 100
LOOPBACK_IP = f"172.{x}.{y}.1"
INTERFACE_NAME = f"Loopback{STUDENT_ID}"

# URL หลักและ Headers
API_BASE_URL = f"https://{ROUTER_IP}/restconf/data"
CONFIG_URL = f"{API_BASE_URL}/ietf-interfaces:interfaces/interface={INTERFACE_NAME}"
STATE_URL = f"{API_BASE_URL}/ietf-interfaces:interfaces-state/interface={INTERFACE_NAME}"
HEADERS = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
BASIC_AUTH = ("admin", "cisco")

def create():
    # ตรวจสอบก่อนว่ามี Interface นี้อยู่แล้วหรือไม่
    check_resp = requests.get(CONFIG_URL, auth=BASIC_AUTH, headers=HEADERS, verify=False)
    if check_resp.status_code == 200:
        return f"Cannot create: Interface loopback {STUDENT_ID}"

    # ถ้าไม่มี ให้สร้างใหม่
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": INTERFACE_NAME, "description": f"Created by student {STUDENT_ID}",
            "type": "iana-if-type:softwareLoopback", "enabled": True,
            "ietf-ip:ipv4": {"address": [{"ip": LOOPBACK_IP, "netmask": "255.255.255.0"}]}
        }
    }
    resp = requests.put(CONFIG_URL, data=json.dumps(yangConfig), auth=BASIC_AUTH, headers=HEADERS, verify=False)
    if resp.status_code == 201: return f"Interface loopback {STUDENT_ID} is created successfully"
    return f"Error creating interface: Status {resp.status_code}"

def delete():
    resp = requests.delete(CONFIG_URL, auth=BASIC_AUTH, headers=HEADERS, verify=False)
    if resp.status_code == 204: return f"Interface loopback {STUDENT_ID} is deleted successfully"
    return f"Cannot delete: Interface loopback {STUDENT_ID}"

def enable():
    yangConfig = {"ietf-interfaces:interface": {"enabled": True}}
    resp = requests.patch(CONFIG_URL, data=json.dumps(yangConfig), auth=BASIC_AUTH, headers=HEADERS, verify=False)
    if resp.status_code in [200, 204]: return f"Interface loopback {STUDENT_ID} is enabled successfully"
    return f"Cannot enable: Interface loopback {STUDENT_ID}"

def disable():
    yangConfig = {"ietf-interfaces:interface": {"enabled": False}}
    resp = requests.patch(CONFIG_URL, data=json.dumps(yangConfig), auth=BASIC_AUTH, headers=HEADERS, verify=False)
    if resp.status_code in [200, 204]: return f"Interface loopback {STUDENT_ID} is shutdowned successfully"
    return f"Cannot shutdown: Interface loopback {STUDENT_ID}"

def status():
    resp = requests.get(STATE_URL, auth=BASIC_AUTH, headers=HEADERS, verify=False)
    if resp.status_code == 200:
        state_data = resp.json().get("ietf-interfaces:interface", {})
        oper_status = state_data.get("oper-status", "down")
        if oper_status == 'up': return f"Interface loopback {STUDENT_ID} is enabled"
        return f"Interface loopback {STUDENT_ID} is disabled"
    elif resp.status_code == 404:
        return f"No Interface loopback {STUDENT_ID}"
    return f"Error getting status: Status {resp.status_code}"