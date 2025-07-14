# Not secret, okay to commit
firebaseConfig = {
    "apiKey": "AIzaSyC28UdMks5G1QQZGAAdMamQ54nV-YRXdrw",
    "authDomain": "ldr-cli-tool.firebaseapp.com",
    "projectId": "ldr-cli-tool",
    "storageBucket": "ldr-cli-tool.firebasestorage.app",
    "messagingSenderId": "915926597401",
    "appId": "1:915926597401:web:f1cf701c1cba63873acf88"
}

FIREBASE_AUTH_ID_TOKEN = None
FIREBASE_USER_ID = None
FIREBASE_AUTH_REFRESH_TOKEN = None
FIREBASE_TOKEN_EXPIRE = None
FIREBASE_SIGNIN_ENDPOINT = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebaseConfig['apiKey']}"
