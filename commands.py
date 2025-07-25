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
    checkTokenRefresh()
    headers = {
        "Authorization": f"Bearer {firebase_config.AUTH_ID_TOKEN}"
    }
    request_payload = {
        "structuredQuery": {
            "from": [{"collectionId": "messages"}],
            "orderBy": [{
                "field": {"fieldPath": "createdAt"},
                "direction": "ASCENDING"
            }]
        }
    }
    response = requests.post(firebase_config.FIRESTORE_QUERY_ENDPOINT, json=request_payload, headers=headers)
    response_payload = response.json()
    if response.status_code == 200:
        messages_exist = False
        for item in response_payload:
            if "document" in item:
                messages_exist = True
                doc = item["document"]
                fields = doc["fields"]
                message = fields["message"]["stringValue"]
                user_id = fields["user_id"]["stringValue"]
                if user_id == firebase_config.USER_ID:
                    rich_print(f"[blue]Me: {message}[/blue]")
                else:
                    rich_print(f"[magenta]Them: {message}[/magenta]")
        
        if not messages_exist:
            print("No recent messages.")
    else:
        print(json.dumps(response_payload, indent=4))


def ping():
    checkTokenRefresh()
    headers = {
        "Authorization": f"Bearer {firebase_config.AUTH_ID_TOKEN}"
    }
    request_payload = {
        "fields": {
            "isValid": {"booleanValue": True},
            "createdAt": {"timestampValue": datetime.now(timezone.utc).isoformat()}
        }
    }
    response = requests.patch(firebase_config.getPingEndpoint(), json=request_payload, headers=headers)
    if response.status_code == 200:
        print("Ping successfully sent!")
    else:
        response_payload = response.json()
        print(json.dumps(response_payload, indent=4))

def getPing():
    checkTokenRefresh()
    headers = {
        "Authorization": f"Bearer {firebase_config.AUTH_ID_TOKEN}"
    }

    ping_file_path = f"projects/{firebase_config.firebaseConfig['projectId']}/databases/(default)/documents/pings/{firebase_config.USER_ID}"
    query_payload = {
        "structuredQuery": {
            "from": [{"collectionId": "pings"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "__name__"},
                    "op": "NOT_EQUAL",
                    "value": {"referenceValue": ping_file_path}
                }
            }
        }
    }


    query_response = requests.post(firebase_config.FIRESTORE_QUERY_ENDPOINT, json=query_payload, headers=headers)
    query_response_payload = query_response.json()
    if query_response.status_code != 200:
        print(json.dumps(query_response_payload, indent=4))
        return
    
    ping_document_exists = False
    ping_document_obj = None
    for item in query_response_payload:
        if "document" in item:
            ping_document_exists = True
            ping_document_obj = item

    if not ping_document_exists:
        return
    
    doc = ping_document_obj["document"]
    name = doc["name"]
    fields = doc["fields"]
    isValid = fields["isValid"]["booleanValue"]
    pingDateString = fields["createdAt"]["timestampValue"]
    if not isValid:
        return
    

    datetime_utc = datetime.fromisoformat(pingDateString.replace("Z", "+00:00"))
    datetime_local = datetime_utc.astimezone()
    local_date = datetime_local.date()
    local_time = datetime_local.strftime("%I:%M %p")
    rich_print(f"\n[bold red]You were sent a :heart:  on {local_date} at {local_time}[/bold red]\n")

    ping_endpoint = f"https://firestore.googleapis.com/v1/{name}"
    params = [
        ("updateMask.fieldPaths", "isValid")
    ]
    patch_payload = {
        "fields": {
            "isValid": {"booleanValue": False}
        }
    }
    patch_response = requests.patch(ping_endpoint, json=patch_payload, headers=headers, params=params)
    patch_response_payload = patch_response.json()
    if patch_response.status_code != 200:
        print(json.dumps(patch_response_payload, indent=4))
    


def addDate(dateString, event):
    checkTokenRefresh()
    headers = {
        "Authorization": f"Bearer {firebase_config.AUTH_ID_TOKEN}"
    }

    # Check if there is an event with the same date and name added

    query_payload = {
        "structuredQuery": {
            "from": [{"collectionId": "dates"}],
            "where": {
                "compositeFilter": {
                    "op": "AND",
                    "filters": [{
                        "fieldFilter": {
                            "field": {"fieldPath": "date"},
                            "op": "EQUAL",
                            "value": {"timestampValue": datetime.strptime(dateString, "%m/%d/%Y").isoformat() + "Z"}
                        }
                    },
                    {
                        "fieldFilter": {
                            "field": {"fieldPath": "event"},
                            "op": "EQUAL",
                            "value": {"stringValue": event}
                        }   
                    }]
                }
            }
        }
    }

    query_response = requests.post(firebase_config.FIRESTORE_QUERY_ENDPOINT, json=query_payload, headers=headers)
    query_response_payload = query_response.json()
    if query_response.status_code != 200:
        print(json.dumps(query_response_payload, indent=4))
        return
    
    event_exists = False
    for item in query_response_payload:
        if "document" in item:
            event_exists = True

    if event_exists:
        print("Failed to add the date. The event already exists!")
        return

    request_payload = {
        "fields": {
            "date": {
                "timestampValue": datetime.strptime(dateString, "%m/%d/%Y").isoformat() + "Z"
            },
            "event": {
                "stringValue": event
            }
        }
    }

    response = requests.post(firebase_config.FIRESTORE_DATES_ENDPOINT, json=request_payload, headers=headers)
    response_payload = response.json()
    if response.status_code != 200:
        print(json.dumps(response_payload, indent=4))
        return
    
    print("Event successfully added!")
    
def viewDates():
    checkTokenRefresh()
    headers = {
        "Authorization": f"Bearer {firebase_config.AUTH_ID_TOKEN}"
    }

    request_payload = {
        "structuredQuery": {
            "from": [{"collectionId": "dates"}]
        }
    }

    response = requests.post(firebase_config.FIRESTORE_QUERY_ENDPOINT, json=request_payload, headers=headers)
    response_payload = response.json()
    if response.status_code != 200:
        print(json.dumps(response_payload, indent=4))
        return
    
    events_exist = False
    for item in response_payload:
        if "document" in item:
            events_exist = True
            doc = item["document"]
            fields = doc["fields"]
            event = fields["event"]["stringValue"]
            dateString = fields["date"]["timestampValue"]
            dateFormatted = datetime.fromisoformat(dateString.replace("Z", "+00:00")).strftime("%m/%d/%Y")
            print(f"Event: {event} Date: {dateFormatted}")

    if not events_exist:
        print("No dates added.")


def getDate():
    checkTokenRefresh()
    headers = {
        "Authorization": f"Bearer {firebase_config.AUTH_ID_TOKEN}"
    }

    
    
    

def quit():
    print("Goodbye!")
    exit(0)

def help():
    usages = [
        "quit - quits the application.",
        "send [italic white]'message'[/italic white] - sends a message to your partner (use quotations if message includes whitespace).",
        "messages - view recent messages with your partner.",
        "ping - ping your partner with a heart.",
        "setupDate [italic]date[/italic] [italic white]'event'[/italic white] - adds a date to your shared calendar for the specified event, date must be in MM/DD/YYYY format. (use quotations if event includes whitespace)",
        "dates - view upcoming dates"
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

