# Not secret, okay to commit
# REPLACE WITH YOUR OWN FIREBASE CONFIG
firebaseConfig = {
    "apiKey": "AIzaSyC28UdMks5G1QQZGAAdMamQ54nV-YRXdrw",
    "authDomain": "ldr-cli-tool.firebaseapp.com",
    "projectId": "ldr-cli-tool",
    "storageBucket": "ldr-cli-tool.firebasestorage.app",
    "messagingSenderId": "915926597401",
    "appId": "1:915926597401:web:f1cf701c1cba63873acf88"
}

AUTH_ID_TOKEN = None
USER_ID = None
AUTH_REFRESH_TOKEN = None
AUTH_ID_TOKEN_EXPIRE = None
AUTH_ID_TOKEN_CREATE_TIME  = None
AUTH_SIGNIN_ENDPOINT = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebaseConfig['apiKey']}"
AUTH_TOKEN_REFRESH_ENDPOINT = f"https://securetoken.googleapis.com/v1/token?key={firebaseConfig['apiKey']}"

FIRESTORE_MESSAGES_ENDPOINT = f"https://firestore.googleapis.com/v1/projects/{firebaseConfig['projectId']}/databases/(default)/documents/messages"

