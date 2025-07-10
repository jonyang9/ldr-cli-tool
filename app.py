import shlex
from datetime import datetime
import commands

COMMANDS = {
    "help": commands.help,
    "quit": commands.quit,
    "send": commands.sendMessage,
    "view": commands.retrieveMessages,
    "ping": commands.ping,
    "setupDate": commands.addDate
}


def validateCommand(args):
    # args is a list of strings entered in the command line
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
    cmd()
        

        
    
    

print("Welcome to ldr-cli, type help for options!")
# Main input loop
while True:
    command_line_input = input("--> ")
    args = shlex.split(command_line_input)
    if validateCommand(args):
        pass

    
        

