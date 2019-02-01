# Link to tutorial https://realpython.com/python-sockets/# tcp-sockets
# For more information about all of these methods see the "server-more_comments" file.

# Import socket to use TCP/IP methods
import socket
from pathlib import Path

hostName = socket.gethostbyname(socket.gethostname())

port = 9999

disconnect = False;

def SplitStrVerk1(_data):
    # We split the string a few times and extract the necessary parts from it.
    # The string's format should be 12;filename:[nameOfFile]::content:[contentFromFile]
    # So with a few operations we should be able to seperate the necessary parts
    _file = _data.split(";")[1]
    _filename, _content = _file.split("::")

    _filename = _filename.split(":")[1]
    _filename = _filename[:-4] + "_new" + _filename[-4:]

    _content = _content.split(":")[1]

    return _filename, _content

def StateManager(data):

    global disconnect

    def SendReady():
        clientSocket.send(b"00;ready")

    state = data.split(";")[0][0]
    substate = data.split(";")[0][1]

    if len(data) > 3:
        message = data.split(";")[1]
    else:
        message = ""

    # We check to see what we got from the client.
    # If we got "Select" then we need to select a file
    # If we got "filename" then we got back a file with a filename and we're gonna copy it
    if state == "0":
        selected = input(message + "\n\nClient choice: ")
        if not int(selected):
            print("Your answer was not recognized. Please try again.")
        else:
            clientSocket.send(bytes(selected+"0", "utf8"))

    if state == "1":
        if substate == "0":
            # Get input from the user
            selected = "11;"
            selected += input(message + "\n\nClient choice: ")
            clientSocket.send(bytes(selected, "utf8"))

        if substate == "2":
            filename, content = SplitStrVerk1(data)
            # Use the Path method to check if the file exists
            file = Path(filename)
            if file.is_file():
                # If the file exists we send the user a message and then flip the disconnect boolean
                print("\n\n ---- File already exists\n\nClosing connection")
                disconnect = True
            else:
                # If the file doesn't exist we create it with the proper filename
                # and then write to it the content from the server
                with open(filename, "x") as file:
                    file.write(content)
                    # When we finish copying the file we send the server another ready message
                    # so we can get the list of filenames again
                    SendReady()

    if state == "2":
        if substate == "0":
            selected = "21;"
            selected += input(message + "\n\nType a filename: ")
            clientSocket.send(bytes(selected, "utf8"))

        if substate == "1":
            filename, content = message.split("::")
            selected = "22;"
            selected += filename + "::"
            selected += input(content + "\n\nPlease type what you wish to overwrite here: ")
            clientSocket.send(bytes(selected, "utf8"))

        if substate == "3":
            question, filename = message.split("::")
            yesOrNo = input(question + "\n\nY/N: ")
            if yesOrNo.lower() not in ["yes", "y", "aye aye cap'n"]:
                SendReady()
            else:
                content = input("\nPlease type what you wish to write in the file: ")
                clientSocket.send(bytes("23;" + filename + "::" + content, "utf8"))

        if substate == "4":
            input(message + "\n\nPress enter to continue")
            SendReady()

    if state == "3":
        if substate == "0":
            selection = "31;"
            selection += input(message + "\n\nSelect difficulty: ")
            clientSocket.send(bytes(selection, "utf8"))
        if substate == "2":
            if message[0] == "|":
                input(message[1:] + "\n\nPress enter to continue")
                SendReady()
            else:
                guess = "32;"
                guess += input(message)
                clientSocket.send(bytes(guess, "utf8"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect((hostName, port))

    # Send "ready" to the server so it can send back the file list
    clientSocket.sendall(b"00;ready")

    while True:
        # If we're ready to disconnect, we send the "disconnect" message to the server
        if disconnect:
            clientSocket.send(b"disconnecting")
            break

        # Receive data from the server and decode using utf8
        data = clientSocket.recv(1024).decode("utf8")

        StateManager(data)