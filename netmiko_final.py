from netmiko import ConnectHandler
from pprint import pprint


device_ip = "10.0.15.62" 


username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_xe",
    "ip": device_ip,
    "username": username,
    "password": password,
}

def gigabit_status():
    ans_list = []
    summary = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show interfaces", use_textfsm=True)
        
        for interface in result:
           
            if "GigabitEthernet" in interface["interface"]:
                status_line = f"{interface['interface']} {interface['status']}"
                ans_list.append(status_line)
                
                if interface["status"] == "up":
                    up += 1
                elif interface["status"] == "down":
                    down += 1
                elif interface["status"] == "administratively down":
                    admin_down += 1
        
        summary = f"{up} up, {down} down, {admin_down} administratively down"
        
        final_ans = ", ".join(ans_list) + f" -> {summary}"
        
        pprint(final_ans)
        return final_ans