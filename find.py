import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your Webex Access Token from the .env file
ACCESS_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")

# Check if the token exists
if not ACCESS_TOKEN:
    print("Error: WEBEX_ACCESS_TOKEN not found.")
    print("Please make sure you have a .env file with your token in it.")
    exit()

# Webex API URL for listing rooms
url = "https://webexapis.com/v1/rooms"

# Headers for the API request, including your authorization token
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Send the GET request to the Webex API
try:
    response = requests.get(url, headers=headers)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Convert the JSON response into a Python dictionary
    rooms = response.json()

    print("🔎 Found the following rooms for your account:")
    print("-" * 50)

    # Loop through the list of rooms and print the title and ID of each one
    if "items" in rooms and rooms["items"]:
        for room in rooms["items"]:
            print(f"Room Name: {room['title']}")
            print(f"Room ID:   {room['id']}\n")
    else:
        print("No rooms found for this account.")
    
    print("-" * 50)
    print("Find the room you need from the list above and copy its Room ID.")

except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")
    if err.response.status_code == 401:
        print("Authentication failed. Your WEBEX_ACCESS_TOKEN might be invalid or expired.")
except Exception as e:
    print(f"An error occurred: {e}")