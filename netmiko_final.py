import os
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
from dotenv import load_dotenv

load_dotenv()

# Device connection parameters
DEVICE_INFO = {
    "device_type": "cisco_ios",
    "host": os.environ.get("ROUTER_HOST"),
    "username": os.environ.get("ROUTER_USER"),
    "password": os.environ.get("ROUTER_PASS"),
}

def get_gigabit_interfaces_status():
    """
    Connects to a device, retrieves interface statuses, and formats them
    into the specified string format.
    Example: "GigabitEthernet1 up, ... -> 1 up, 2 down, 1 administratively down"
    """
    try:
        with ConnectHandler(**DEVICE_INFO) as connection:
            # Send command and parse the output using TextFSM
            interfaces_data = connection.send_command("show ip interface brief", use_textfsm=True)

            if not interfaces_data:
                return "Error: Could not retrieve interface information from the device."

            status_list = []
            status_counts = {"up": 0, "down": 0, "administratively down": 0}

            # Loop through each interface to build the status list and count statuses
            for interface in interfaces_data:
                if 'GigabitEthernet' in interface.get('interface', ''):
                    status = interface.get('status', 'unknown')
                    
                    # Add "interface_name status" to the list
                    status_list.append(f"{interface['interface']} {status}")
                    
                    # Increment the counter for the corresponding status
                    if status in status_counts:
                        status_counts[status] += 1

            # Join the individual interface statuses with a comma
            details_part = ", ".join(status_list)
            
            # Create the summary part of the string
            summary_part = (f"{status_counts['up']} up, "
                            f"{status_counts['down']} down, "
                            f"{status_counts['administratively down']} administratively down")

            # Combine both parts into the final desired format
            final_output = f"{details_part} -> {summary_part}"
            
            print(f"Generated status string: {final_output}")
            return final_output

    except (NetmikoAuthenticationException, NetmikoTimeoutException) as e:
        error_message = f"Connection Error: {e}"
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message