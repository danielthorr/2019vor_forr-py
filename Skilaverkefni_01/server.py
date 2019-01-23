# Link to tutorial https://realpython.com/python-sockets/# tcp-sockets
# For more information about all of these methods see the "server-more_comments" file.

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

try:
    #hostName = socket.getfqdn() # <- didn't work for me at home, but works at school. Something about proxy maybe.
    hostName = socket.gethostbyname(socket.gethostname())
except socket.gaierror:
    print("Error getting host ip/name")

# Establish a port to be used on both the server and client
port = 9999

# A function we use to parse some information from the client
# And then to send a file back (only works for txt files at the moment)
def SendFile(_data):
    # The file we receive from the client looks like this "answer:[filename]"
    # so we split the string and choose only the second half which contains the filename
    answer = _data.split(":")[1]

    # Checking the file extension
    if answer.lower()[-4:] != ".txt":
        answer += ".txt"
        print("User selected to receive: " + answer)

    tmpPath = Path("archive") / answer

    with open(tmpPath, "rb") as file:
        # Send the file to the client
        conn.sendto(bytes("filename:" + answer + ";content:", "utf8") + file.read(), addr)


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
