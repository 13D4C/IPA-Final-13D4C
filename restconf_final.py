import json
import requests
requests.packages.urllib3.disable_warnings()

ROUTER_IP = "10.0.15.61"  
STUDENT_ID = "66070216" 

last_three = int(STUDENT_ID[-3:])
x, y = divmod(last_three, 100)
if STUDENT_ID[-3] == '0':
    x = int(STUDENT_ID[-3:-1])
    y = int(STUDENT_ID[-1])
else:
    x = int(STUDENT_ID[-3])
    y = int(STUDENT_ID[-2:])

LOOPBACK_IP = f"172.{x}.{y}.1"
API_URL = f"https://{ROUTER_IP}/restconf/data/ietf-interfaces:interfaces/interface=Loopback{STUDENT_ID}"

headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
basicauth = ("admin", "cisco")

def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": f"Loopback{STUDENT_ID}", "description": "Created via RESTCONF",
            "type": "iana-if-type:softwareLoopback", "enabled": True,
            "ietf-ip:ipv4": {"address": [{"ip": LOOPBACK_IP, "netmask": "255.255.255.0"}]}
        }
    }
    resp = requests.put(API_URL, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 201: return f"Interface loopback {STUDENT_ID} is created successfully"
    if resp.status_code == 204: return f"Cannot create: Interface loopback {STUDENT_ID}"
    return f"Error creating: {resp.status_code}"

def delete():
    resp = requests.delete(API_URL, auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204: return f"Interface loopback {STUDENT_ID} is deleted successfully"
    return f"Cannot delete: Interface loopback {STUDENT_ID}"

def enable():
    yangConfig = {"ietf-interfaces:interface": {"name": f"Loopback{STUDENT_ID}", "enabled": True}}
    resp = requests.patch(API_URL, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204: return f"Interface loopback {STUDENT_ID} is enabled successfully"
    return f"Cannot enable: Interface loopback {STUDENT_ID}"

def disable():
    yangConfig = {"ietf-interfaces:interface": {"name": f"Loopback{STUDENT_ID}", "enabled": False}}
    resp = requests.patch(API_URL, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204: return f"Interface loopback {STUDENT_ID} is shutdowned successfully"
    return f"Cannot shutdown: Interface loopback {STUDENT_ID}"

def status():
    api_url_status = f"https://{ROUTER_IP}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback{STUDENT_ID}"
    resp = requests.get(api_url_status, auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        state = resp.json().get("ietf-interfaces:interface", {})
        admin_status = state.get("admin-status", "down")
        oper_status = state.get("oper-status", "down")
        if admin_status == 'up' and oper_status == 'up': return f"Interface loopback {STUDENT_ID} is enabled"
        return f"Interface loopback {STUDENT_ID} is disabled"
    elif resp.status_code == 404:
        return f"No Interface loopback {STUDENT_ID}"
    return f"Error getting status: {resp.status_code}"