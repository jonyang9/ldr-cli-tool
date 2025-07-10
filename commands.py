from rich import print as rich_print

def sendMessage(message):
    pass

def retrieveMessages():
    pass

def ping():
    pass

def addDate():
    pass

def quit():
    exit(0)

def help():
    usages = [
        "quit - quits the application.",
        "send [italic]message[/italic] - sends a message to your partner.",
        "view - view recent messages with your partner.",
        "ping - ping your partner with a heart.",
        "setupDate [italic]date[/italic] - adds a date to your shared calendar, date must be in MM/DD/YYYY format."
    ]
    rich_print("\n".join(usages))

