import shlex
from datetime import datetime
import commands
import getpass
import requests
import firebase_config

COMMANDS = {
    "help": commands.help,
    "quit": commands.quit,
    "send": commands.sendMessage,
    "view": commands.retrieveMessages,
    "ping": commands.ping,
    "setupDate": commands.addDate
}


def validateCommand(args):
    # returns True if the command is valid, false otherwise
    if not args:
        return False
    if args[0] not in COMMANDS:
        print(f"{args[0]} is not a valid command, type help for usage")
        return False
    match args[0]:
        case "help" | "quit" | "view" | "ping":
            if len(args) > 1:
                print(f"Command failed. Too many arguments to the {args[0]} command.")
                return False
        case "send":
            if len(args) != 2:
                print("Command failed. Incorrect number of arguments to the send command.")
                return False
        case "setupDate":
            if len(args) != 2:
                print("Command failed. Incorrect number of arguments to the setupDate command.")
                return False
            try:
                date_obj = datetime.strptime(args[1], "%m/%d/%Y")
                if (date_obj.date() < datetime.now().date()):
                    print("Command failed. The given date is in the past!")
                    return False
            except ValueError:
                print("Command failed. Given date is not a correctly formatted date.")
                return False
    return True



def runCommand(args):
    cmd = COMMANDS[args[0]]
    if args[0] in ["help", "quit", "view", "ping"]:
        cmd()
    elif args[0] in ["send", "setupDate"]:
        cmd(args[1])
    


print("Welcome to ldr-cli, please complete the authentication steps. Type 'quit' anytime to exit.")

# Authentication loop
while True:
    while True:
        email = input("Enter your email: ")
        if email.strip().lower() == "quit":
            exit(0)
        print(f"Your email is: '{email}'")

        while True:
            yes_or_no = input("Is this correct? (yes/no) ").strip().lower()

            if yes_or_no.strip().lower() == "quit":
                exit(0)
            
            if yes_or_no in ("yes", "no"):
                break
            else:
                print("Please answer 'yes' or 'no'. ")

        if yes_or_no == "yes":
            break
    
    while True:
        password = getpass.getpass("Enter your password: ")
        confirm_password = getpass.getpass("Confirm your password: ")
        if password != confirm_password:
            print("Passwords don't match. Please try again.")
        else:
            break
    
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
        break
    else:
        error = response_payload["error"]["message"]
        print(f"Error with sign-in: {error}")



    
print("You've signed in! Type help for options.")

commands.getPing()

# Main command input loop
while True:
    command_line_input = input("--> ")
    try:
        args = shlex.split(command_line_input)
        if validateCommand(args):
            runCommand(args)
        
    except ValueError as error:
        print(f"Error parsing command: {error}")
    
