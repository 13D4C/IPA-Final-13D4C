# --------------------------------------------------------------
# Import libraries and connect to device
# --------------------------------------------------------------
import os
import xmltodict
from ncclient import manager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Constants & Configuration ---
STUDENT_ID = "66070216"
LOOPBACK_INTERFACE_NAME = f"Loopback{STUDENT_ID}"

# Establish a connection to the network device
try:
    netconf_manager = manager.connect(
        host=os.environ.get("ROUTER_HOST"),
        port=830,
        username=os.environ.get("ROUTER_USER"),
        password=os.environ.get("ROUTER_PASS"),
        hostkey_verify=False
    )
except Exception as e:
    print(f"Failed to connect to device: {e}")
    exit()

# --------------------------------------------------------------
# Core functions
# --------------------------------------------------------------

def create_loopback():
    """Creates a new loopback interface using NETCONF."""
    netconf_payload = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{LOOPBACK_INTERFACE_NAME}</name>
                    <description>{STUDENT_ID} Loopback interface</description>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                        <address>
                            <ip>172.2.17.1</ip>
                            <netmask>255.255.255.0</netmask>
                        </address>
                    </ipv4>
                </interface>
            </interfaces>
        </config>
    """
    try:
        if interface_exists():
            raise Exception(f"Interface {LOOPBACK_INTERFACE_NAME} already exists.")
        
        reply = netconf_edit_config(netconf_payload)
        if '<ok/>' in reply.xml:
            return f"Interface loopback {STUDENT_ID} is created successfully."
        else:
            raise Exception("NETCONF reply was not OK.")
    except Exception as e:
        print(f"Error in create_loopback: {e}")
        return f"Cannot create: Interface loopback {STUDENT_ID}."


def delete_loopback():
    """Deletes the loopback interface using NETCONF."""
    netconf_payload = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation="delete">
                    <name>{LOOPBACK_INTERFACE_NAME}</name>
                </interface>
            </interfaces>
        </config>
    """
    try:
        if not interface_exists():
            raise Exception(f"Interface {LOOPBACK_INTERFACE_NAME} does not exist.")
        
        reply = netconf_edit_config(netconf_payload)
        if '<ok/>' in reply.xml:
            return f"Interface loopback {STUDENT_ID} is deleted successfully."
        else:
            raise Exception("NETCONF reply was not OK.")
    except Exception as e:
        print(f"Error in delete_loopback: {e}")
        return f"Cannot delete: Interface loopback {STUDENT_ID}."


def enable_loopback():
    """Enables the loopback interface using NETCONF."""
    netconf_payload = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{LOOPBACK_INTERFACE_NAME}</name>
                    <enabled>true</enabled>
                </interface>
            </interfaces>
        </config>
    """
    try:
        if not interface_exists():
            raise Exception(f"Interface {LOOPBACK_INTERFACE_NAME} does not exist.")
        
        reply = netconf_edit_config(netconf_payload)
        if '<ok/>' in reply.xml:
            return f"Interface loopback {STUDENT_ID} is enabled successfully."
        else:
            raise Exception("NETCONF reply was not OK.")
    except Exception as e:
        print(f"Error in enable_loopback: {e}")
        return f"Cannot enable: Interface loopback {STUDENT_ID}."


def disable_loopback():
    """Disables the loopback interface using NETCONF."""
    netconf_payload = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{LOOPBACK_INTERFACE_NAME}</name>
                    <enabled>false</enabled>
                </interface>
            </interfaces>
        </config>
    """
    try:
        if not interface_exists():
            raise Exception(f"Interface {LOOPBACK_INTERFACE_NAME} does not exist.")

        reply = netconf_edit_config(netconf_payload)
        if '<ok/>' in reply.xml:
            return f"Interface loopback {STUDENT_ID} is shutdown successfully."
        else:
            raise Exception("NETCONF reply was not OK.")
    except Exception as e:
        print(f"Error in disable_loopback: {e}")
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}."


def get_loopback_status():
    """Gets the status of the loopback interface using NETCONF."""
    netconf_filter = f"""
        <filter>
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>{LOOPBACK_INTERFACE_NAME}</name></interface>
            </interfaces-state>
        </filter>
    """
    try:
        reply = netconf_manager.get(filter=netconf_filter)
        reply_dict = xmltodict.parse(reply.xml)
        interface_data = reply_dict.get("rpc-reply", {}).get("data")

        if interface_data:
            interface_state = interface_data["interfaces-state"]["interface"]
            admin_status = interface_state["admin-status"]
            oper_status = interface_state["oper-status"]
            
            if admin_status == 'up' and oper_status == 'up':
                return f"Interface loopback {STUDENT_ID} is enabled."
            elif admin_status == 'down' and oper_status == 'down':
                return f"Interface loopback {STUDENT_ID} is disabled."
        else:
            return f"No Interface loopback {STUDENT_ID}."
    except Exception as e:
       print(f"Error in get_loopback_status: {e}")
       return f"Could not retrieve status for Interface loopback {STUDENT_ID}."

# --------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------

def netconf_edit_config(payload):
    """Applies configuration changes using edit-config."""
    return netconf_manager.edit_config(target="running", config=payload)


def netconf_get_config(filter_payload):
    """Retrieves configuration data using get-config."""
    return netconf_manager.get_config(source="running", filter=filter_payload)


def interface_exists():
    """Checks if the specific loopback interface exists."""
    filter_payload = f"""
        <filter>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface><name>{LOOPBACK_INTERFACE_NAME}</name></interface>
            </interfaces>
        </filter>
    """
    result_xml = netconf_get_config(filter_payload).xml
    return LOOPBACK_INTERFACE_NAME in result_xml