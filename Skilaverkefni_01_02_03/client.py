# Link to tutorial https://realpython.com/python-sockets/# tcp-sockets
# For more information about all of these methods see the "server-more_comments" file.

# Import socket to use TCP/IP methods
import socket
from pathlib import Path

hostName = socket.gethostbyname(socket.gethostname())

port = 9999

def StateManager(data):

    def SendReady():
        clientSocket.send(b"00;ready")

    state = data.split(";")[0]
    message = data.split(";")[1]

    # We check to see what we got from the client.
    # If we got "Select" then we need to select a file
    # If we got "filename" then we got back a file with a filename and we're gonna copy it
    if state == "00":
        selected = input(message + "\n\nClient choice: ")
        if not int(selected):
            print("Your answer was not recognized. Please try again.")
        else:
            clientSocket.send(bytes(selected+"0", "utf8"))
    if state == "10":
        # Get input from the user
        selected = input(message + "\n\nClient choice: ")
        if not int(selected):
            print("Your answer was not recognized. Please try again.")
        else:
            clientSocket.send(bytes(selected, "utf8"))
            # Send our answer back to the server, formatted in a way the server can deconstruct
            clientSocket.send(b"answer:" + bytes(selected, "utf8"))

    if state == "20":
        selected = "21"
        selected += input(message + "\n\nType a filename:")
        clientSocket.send(bytes(selected, "utf8"))

    if state == "21":
        SendReady()

    if state == "30":
        conn.sendto(bytes("30;", "utf8"), addr)

    if state == "31":

disconnect = False;

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

        if data[0:8] == "filename":
            # We split the data into "filename:[filename]" and "content:[content]"
            filename, content = data.split(";")
            # Split the filename string and grab the filename itself
            filename = filename.split(":")[1]
            # Split the content and grab the content itself
            content = content.split(":")[1]
            # Do some weird str methods to insert "_new" before the extension
            filename = filename[:-4]+"_new"+filename[-4:]
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
                    clientSocket.send(b"0")
