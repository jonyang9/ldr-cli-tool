# Run as a cron job to delete old messages and events

import requests
import firebase_config
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json

load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

request_payload = {
    "email": email,
    "password": password,
    "returnSecureToken": True
}

response = requests.post(firebase_config.AUTH_SIGNIN_ENDPOINT, json=request_payload)
response_payload = response.json()
if response.status_code == 200:
    firebase_config.AUTH_ID_TOKEN_CREATE_TIME = datetime.now()
    firebase_config.AUTH_ID_TOKEN = response_payload["idToken"]
    firebase_config.AUTH_REFRESH_TOKEN = response_payload["refreshToken"]
    firebase_config.USER_ID = response_payload["localId"]
    firebase_config.AUTH_ID_TOKEN_EXPIRE = int(response_payload["expiresIn"]) 
else:
    error = response_payload["error"]["message"]
    print(f"Error with sign-in: {error}")

headers = {
    "Authorization": f"Bearer {firebase_config.AUTH_ID_TOKEN}"
}

# delete old messages
days_old = 30

today_date = datetime.now().date()
cutoff = today_date - timedelta(days=days_old)
cutoff_timestamp = cutoff.isoformat() + "T00:00:00Z"
print(cutoff_timestamp)

query_payload = {
  "structuredQuery": {
    "from": [{ "collectionId": "messages" }],
    "where": {
      "fieldFilter": {
        "field": { "fieldPath": "createdAt" },
        "op": "LESS_THAN",
        "value": {
          "timestampValue": cutoff_timestamp
        }
      }
    }
  }
}

response = requests.post(firebase_config.FIRESTORE_QUERY_ENDPOINT, json=query_payload, headers=headers)
response_payload = response.json()
if response.status_code != 200:
    print(json.dumps(response_payload, indent=4))

url_base = "https://firestore.googleapis.com/v1/"

for item in response_payload:
    if "document" in item:
        doc = item["document"]
        name = doc["name"]
        endpoint = url_base + name
        delete_response = requests.delete(endpoint, headers=headers)
        if delete_response.status_code == 200:
            print("Deleted a message.")

today_timestamp = today_date.isoformat() + "T00:00:00Z"
print(today_timestamp)

query_payload = {
  "structuredQuery": {
    "from": [{ "collectionId": "dates" }],
    "where": {
      "fieldFilter": {
        "field": { "fieldPath": "date" },
        "op": "LESS_THAN",
        "value": {
          "timestampValue": today_timestamp
        }
      }
    }
  }
}

response = requests.post(firebase_config.FIRESTORE_QUERY_ENDPOINT, json=query_payload, headers=headers)
response_payload = response.json()
if response.status_code != 200:
    print(json.dumps(response_payload, indent=4))

for item in response_payload:
    if "document" in item:
        doc = item["document"]
        name = doc["name"]
        endpoint = url_base + name
        delete_response = requests.delete(endpoint, headers=headers)
        if delete_response.status_code == 200:
            print("Deleted a date.")
