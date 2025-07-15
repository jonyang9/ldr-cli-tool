from rich import print as rich_print
import requests
from datetime import datetime, timezone
import firebase_config
import json

def sendMessage(message):
    checkTokenRefresh()
    headers = {
        "Authorization": f"Bearer {firebase_config.AUTH_ID_TOKEN}"
    }
    request_payload = {
        "fields": {
            "user_id": {"stringValue": firebase_config.USER_ID},
            "message": {"stringValue": message},
            "createdAt": {"timestampValue": datetime.now(timezone.utc).isoformat()}
        }
    }
    response = requests.post(firebase_config.FIRESTORE_MESSAGES_ENDPOINT, json=request_payload, headers=headers)
    response_payload = response.json()
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(json.dumps(response_payload, indent=4))

def retrieveMessages():
    print("running view command")
    pass

def ping():
    print("running ping command")
    pass

def addDate(dateString):
    print("running setupDate command")
    pass

def quit():
    print("Goodbye!")
    exit(0)

def help():
    usages = [
        "quit - quits the application.",
        "send [italic white]'message'[/italic white] - sends a message to your partner (use quotations if message includes whitespace).",
        "view - view recent messages with your partner.",
        "ping - ping your partner with a heart.",
        "setupDate [italic]date[/italic] - adds a date to your shared calendar, date must be in MM/DD/YYYY format."
    ]
    rich_print("\n".join(usages))

def checkTokenRefresh():
    # If the Firebase ID Token is expired, refresh it
    now = datetime.now()
    diff = now - firebase_config.AUTH_ID_TOKEN_CREATE_TIME
    secs = diff.total_seconds()
    if secs > firebase_config.AUTH_ID_TOKEN_EXPIRE:
        request_data = {
            "grant_type": "refresh_token",
            "refresh_token": firebase_config.AUTH_REFRESH_TOKEN
        }
        response = requests.post(firebase_config.AUTH_TOKEN_REFRESH_ENDPOINT, data=request_data)
        response_payload = response.json()
        if response.status_code == 200:
            firebase_config.AUTH_ID_TOKEN_CREATE_TIME = datetime.now()
            firebase_config.AUTH_ID_TOKEN = response_payload["id_token"]
            firebase_config.AUTH_ID_TOKEN_EXPIRE = int(response_payload["expires_in"])
            firebase_config.AUTH_REFRESH_TOKEN = response_payload["refresh_token"]
            firebase_config.USER_ID = response_payload["user_id"]
        else:
            error = response_payload["error"]["message"]
            print(f"Error with sign-in: {error}")

