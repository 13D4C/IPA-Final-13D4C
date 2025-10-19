#######################################################################################
# Yourname: 13D4C
# Your student ID: 66070216
# Your GitHub Repo: https://github.com/13D4C/IPA-Final-13D4C

#######################################################################################
# 1. Import libraries
import os, time, json, requests
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Import modules
import restconf_final 
import netmiko_final
import ansible_final

load_dotenv() 

#######################################################################################
# 2. Assign Webex access token
ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")

#######################################################################################
# 3. Prepare parameters

WEBEX_ROOM_ID = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vYmQwODczMTAtNmMyNi0xMWYwLWE1MWMtNzkzZDM2ZjZjM2Zm"
STUDENT_ID = "66070216"
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

if not ACCESS_TOKEN or not WEBEX_ROOM_ID or "YOUR" in WEBEX_ROOM_ID:
    print("FATAL: Please set WEBEX_ACCESS_TOKEN in .env and edit WEBEX_ROOM_ID in the script.")
    exit()

print("Bot started... Listening for commands.")
while True:
    time.sleep(1)
    getParameters = {"roomId": WEBEX_ROOM_ID, "max": 1}
    getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# 4. Get the latest message
    try:
        r = requests.get("https://webexapis.com/v1/messages", params=getParameters, headers=getHTTPHeader)
        if not r.status_code == 200:
            print(f"Error getting message: {r.status_code}")
            continue

        json_data = r.json()
        if not json_data["items"]:
            continue

        message = json_data["items"][0]["text"]
        
        # Check if the message is a command for our bot
        magic_word = f"/{STUDENT_ID} "
        if not message.startswith(magic_word):
            continue

        print(f"Received message: {message}")
        command = message.split(" ")[1].strip()
        print(f"Executing command: '{command}'")

# 5. Execute command
        responseMessage = ""
        if command == "create": responseMessage = restconf_final.create()
        elif command == "delete": responseMessage = restconf_final.delete()
        elif command == "enable": responseMessage = restconf_final.enable()
        elif command == "disable": responseMessage = restconf_final.disable()
        elif command == "status": responseMessage = restconf_final.status()
        elif command == "gigabit_status": responseMessage = netmiko_final.gigabit_status()
        elif command == "showrun": responseMessage = ansible_final.showrun()
        else: responseMessage = "Error: Unknown command"
        
        print(f"Response to send: {responseMessage}")

# 6. Post response to Webex
        postHTTPHeaders = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        
        if command == "showrun" and responseMessage == 'ok':
            filename = f"show_run_{STUDENT_ID}_csr1kv.txt"
            m = MultipartEncoder(
                fields={"roomId": WEBEX_ROOM_ID, "text": "Show running-config result:",
                        "files": (filename, open(filename, 'rb'), 'text/plain')}
            )
            postData = m
            postHTTPHeaders["Content-Type"] = m.content_type
        else:
            postData = json.dumps({"roomId": WEBEX_ROOM_ID, "text": responseMessage})
            postHTTPHeaders["Content-Type"] = "application/json"

        r = requests.post("https://webexapis.com/v1/messages", data=postData, headers=postHTTPHeaders)
        if not r.status_code == 200:
            print(f"Error posting message: {r.status_code} {r.text}")

    except Exception as e:
        print(f"An error occurred: {e}")