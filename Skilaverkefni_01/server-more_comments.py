# Link to tutorial https://realpython.com/python-sockets/# tcp-sockets

# Import socket to use TCP/IP methods
import socket
# Import Path from pathlib to properly resolve paths
from pathlib import Path
#from os import listdir # - this may be used later

# Short function to initialize the files we use in this project
def InitFiles():
    path = Path("archive")
    filenames = ["file1.txt", "file2.txt", "file3.txt"]
    for x in range(0,3):
        tmpPath = path / filenames[x]
        if not tmpPath.is_file():
            if x == 0:
                textToWrite = "This is file1.\n\nHere is some additional flavor text.\nFile 1."
            elif x == 1:
                textToWrite = "This is file2.\n\nHere is some additional flavor text.\nFile 2."
            elif x == 2:
                textToWrite = "This is file3.\n\nHere is some additional flavor text.\nFile 3."
            else:
                textToWrite = "Something went wrong cap'n!"
            with open(tmpPath, "w") as file:
                file.write(textToWrite)

# Call the function to initialize the files
InitFiles()


# Create a socket object for the connection
# socket.getfqdn() looks for the domain with the name in the arguments. If no name is given it finds the localhost
try:
    #hostName = socket.getfqdn() # <- didn't work for me at home, but works at school. Something about proxy maybe.
    hostName = socket.gethostbyname(socket.gethostname())
except socket.gaierror:
    print("Error getting host ip/name")

# - NOTE: hostnames are resolved through DNS so results can be non-deterministic. Use numeric host addresses for deterministic behavior

# Establish a port, doesn't matter what it is but it need to be the same in the code that will try to connect
port = 9999

# A function we use to parse some information from the client
# And then to send a file back (only works for txt files at the moment)
def SendFile(_data):
    # The file we receive from the client looks like this "answer:[filename]"
    # so we split the string and choose only the second half which contains the filename
    answer = _data.split(":")[1]
    # This if statement just checks if the file extension is missing then appends it
    if answer.lower()[-4:] != ".txt":
        answer += ".txt"
        print("User selected to receive: " + answer)
    # For some reason the path wants to be stored in a separate variable to be used
    # Note that the files we send to the client are stored in a different folder
    tmpPath = Path("archive") / answer
    # We open the file in "read-byte" mode
    with open(tmpPath, "rb") as file:
        # And we send the filename as well as the contents of the file to the user
        conn.sendto(bytes("filename:" + answer + ";content:", "utf8") + file.read(), addr)


# socket.socket creates a socket object that supports the context manager type so you can use it in a with statement
# AF_INET is the internet address family for IPv4
# SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    # Bind to the port - read below for more thorough info on this.
    # Empty string means that the socket is going to accept any connection
    serverSocket.bind(("", port))

    # We need to listen() to the socket to be able to accept new connections
    # starting in Python 3.5, it's optional to put in a value.
    # A default backlog value is chosen if empty
    serverSocket.listen()

    # accept() is a "blocking call" that holds an incoming connection
    # until system resources are ready then returns
    # a new socket object (type: tuple) representing the connection.
    conn, addr = serverSocket.accept()
    # One thing that is imperative to understand is that accept makes a new socket object
    # so now we need to use THAT socket to communicate with the client.
    # It's NOT THE SAME SOCKET as we have been using up until now.

    # Use that socket object just like we used our original socket in a "with" statement
    with conn:
        print("\nPC ", addr, " successfully connected.\n")
        # We loop indefinitely over blocking calls to conn.recv().
        # We receive data from the client and store it in our data variable
        # and then send it back using conn.sendall(data) or other conn.send() method
        while True:
            # We receive data in bytes, decode them to the utf8 standard
            data = conn.recv(1024).decode("utf8")

            # The client sends this message if it's ready to disconnect
            if data == "disconnecting":
                print("client is disconnecting")
                # This break statements breaks our while loop which keeps the connection open
                break

            # The client sends a ready signal whenever we should "start over" (or begin) and send the file list
            if data == "ready":
                print("Client is ready")
                # Send a simple string to our client which displays the files that can be sent over
                conn.sendto(bytes("Select file:\n\nfile1.txt\nfile2.txt\nfile3.txt", "utf8"), addr)
            # We check to see if the client has sent us it's answer.
            # The string format from the client is "answer:[filename]" so we check to see if the string contains "answer:"
            if data[0:7] == "answer:":
                print("Received answer from client")
                # Here we send the data variable to our function to check the client's answer and send back a file
                SendFile(data)
                print("File sent\n")


#   --------    Extra information   --------    #
#   bind() is used to associate the socket with a specific network interface and port number.
#   The values passed to bind() depend on the address family of the socket. In this example, socket.AF_INET expects a 2-tuple: (host, port).
#   host can be a hostname, IP address, or empty string. If an IP address is used, it should be IPv4.1 27.0.0.1 is the loopback interface, so only processes on the host will be able to connect to the server. If you pass an empty string, the server will accept connections on all available IPv4 interfaces.
#   port should be an integer from 1-65535 (0 is reserved). It’s the TCP port number to accept connections on from clients. Some systems may require superuser privileges if the port is < 1024.
