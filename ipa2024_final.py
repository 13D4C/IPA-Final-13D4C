#######################################################################################
# Yourname: Atibodee Kuiprasert
# Your student ID: 66070216
#
# *** นี่คือเวอร์ชันที่แก้ไข I/O Error แล้ว ***
#######################################################################################

# 1. Import libraries
import os
import time
import json
import requests
import glob
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Import functions from other modules
from restconf_final import create_interface, delete_interface, enable_interface, disable_interface, get_interface_status
from netmiko_final import get_gigabit_interfaces_status
from ansible_final import run_show_command
#######################################################################################

# 2. Load environment variables
load_dotenv()
ACCESS_TOKEN = os.environ.get("WEBX_ACCESS_TOKEN")
ROOM_ID = os.environ.get("ROOM_ID")
STUDENT_ID = "66070216"
#######################################################################################

# 3. Main loop
print("Bot is running... Waiting for commands.")
while True:
    time.sleep(1) 

    get_parameters = {"roomId": ROOM_ID, "max": 1}
    http_headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        response = requests.get(
            "https://webexapis.com/v1/messages",
            params=get_parameters,
            headers=http_headers,
        )
        response.raise_for_status()

        json_data = response.json()
        if not json_data.get("items"):
            continue 

        latest_message = json_data["items"][0]["text"]
        
        # We only process new commands, not the bot's own responses.
        if latest_message.startswith(f"/{STUDENT_ID}"):
            print(f"Received message: {latest_message}")
            command = latest_message.split()[-1]
            print(f"Executing command: {command}")
            response_message = "" 

            # 5. Execute command
            if command == "create":
                response_message = create_interface()
            elif command == "delete":
                response_message = delete_interface()
            elif command == "enable":
                response_message = enable_interface()
            elif command == "disable":
                response_message = disable_interface()
            elif command == "status":
                response_message = get_interface_status()
            elif command == "gigabit_status":
                response_message = get_gigabit_interfaces_status()
            elif command == "showrun":
                response_message = run_show_command()
            else:
                response_message = "Error: Unknown command."

            # 6. Post the response
            # --- START OF THE FIX ---
            if command == "showrun" and response_message == 'ok':
                run_files = glob.glob("show_run_*.txt")
                if not run_files:
                    response_message = "Error: showrun file not found."
                else:
                    latest_file = max(run_files, key=os.path.getctime)
                    
                    # Open the file and send the request INSIDE this 'with' block
                    with open(latest_file, "rb") as file_content:
                        multipart_data = MultipartEncoder({
                            "roomId": ROOM_ID,
                            "text": "Here is the running configuration:",
                            "files": (os.path.basename(latest_file), file_content, "text/plain"),
                        })
                        
                        post_headers = {
                            "Authorization": f"Bearer {ACCESS_TOKEN}",
                            "Content-Type": multipart_data.content_type
                        }
                        
                        # The POST request is now INSIDE the 'with' block
                        requests.post(
                            "https://webexapis.com/v1/messages",
                            data=multipart_data,
                            headers=post_headers
                        ).raise_for_status()
                    
                    print("File sent successfully.")
                    # We set response_message to None because the file has already been sent
                    response_message = None 
            
            # If response_message is not None, send it as a simple text message
            if response_message:
                post_headers = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }
                post_data = json.dumps({"roomId": ROOM_ID, "text": response_message})
                requests.post(
                    "https://webexapis.com/v1/messages",
                    data=post_data,
                    headers=post_headers
                ).raise_for_status()
                print(f"Text response '{response_message}' sent successfully.")

            # To avoid re-processing the same command, we need a way to mark it as done.
            # A simple approach is to assume the last message is the one we just processed.
            # In a real-world bot, you'd track message IDs.

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the Webex API request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")