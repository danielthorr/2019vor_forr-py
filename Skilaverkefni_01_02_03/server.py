# Link to tutorial https://realpython.com/python-sockets/# tcp-sockets
# For more information about all of these methods see the "server-more_comments" file.

# Import socket to use TCP/IP methods
import socket
# Import Path from pathlib to properly resolve paths
from pathlib import Path
#from os import listdir # - this may be used later

import server_methods as ServerMethod

# Call the function to initialize the files
ServerMethod.InitFiles()

try:
    # hostName = socket.getfqdn() # <- didn't work for me at home, but works at school. Something about proxy maybe.
    hostName = socket.gethostbyname(socket.gethostname())
except socket.gaierror:
    print("Error getting host ip/name")

# Establish a port to be used on both the server and client
port = 9999

mainMenu = ("00;This is the initial screen, please select one of the option listed below:"
            "\n"
            "\n\t1. Verkefni 01 - Receive file from server"
            "\n\t2. Verkefni 02 - Receive file, edit locally, then send modified file back"
            "\n\t3. Verkefni 03 - Play a game of hangman"
            )


def StateManager(data):
    # We declare our state from only the first character from the client.
    # This will be our state. (See "mainMenu" variable for the other states)
    state = data.split(";")[0][0]
    substate = data.split(";")[0][1]
    if len(data) > 3:
        message = data.split(";")[1]
    else:
        message = ""

    # We use 0 as a "ready" signal, which means that the client is either ready to begin or ready
    # to go back to the "main menu"
    if state == "0":
        print("Client is ready")
        # Send a simple string to our client which displays the files that can be sent over
        conn.sendto(bytes(mainMenu, "utf8"), addr)

    if state == "1":
        toSend = ServerMethod.Verkefni1(substate, message)
        conn.sendto(toSend, addr)

    if state == "2":
        toSend = ServerMethod.Verkefni2(substate, message)
        conn.sendto(toSend, addr)
        print("justtopause")

    if state == "3":
        toSend = ServerMethod.Verkefni3(substate, message)
        conn.sendto(toSend, addr)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    # Empty string means that the socket is going to accept any connection
    serverSocket.bind(("", port))

    # We need to listen() to the socket to be able to accept new connections
    # A default backlog value is chosen if empty
    serverSocket.listen()

    conn, addr = serverSocket.accept()

    with conn:
        print("\nPC ", addr, " successfully connected.\n")

        while True:
            # We receive data in bytes, decode them to the utf8 standard
            data = conn.recv(1024).decode("utf8")

            # The client sends this message if it's ready to disconnect
            if data == "disconnecting":
                print("client is disconnecting")
                # This break statements breaks our while loop which keeps the connection open
                break

            # We send our data through to our "state manager" - which decides what state we are in
            # In other words, when the clients selects an option to run,
            # that is the state of our server in relation to the client
            StateManager(data)

#   --------    Extra information   --------    #
#   bind() is used to associate the socket with a specific network interface and port number.
#   The values passed to bind() depend on the address family of the socket. In this example, socket.AF_INET expects a 2-tuple: (host, port).
#   host can be a hostname, IP address, or empty string. If an IP address is used, it should be IPv4.1 27.0.0.1 is the loopback interface, so only processes on the host will be able to connect to the server. If you pass an empty string, the server will accept connections on all available IPv4 interfaces.
#   port should be an integer from 1-65535 (0 is reserved). It’s the TCP port number to accept connections on from clients. Some systems may require superuser privileges if the port is < 1024.