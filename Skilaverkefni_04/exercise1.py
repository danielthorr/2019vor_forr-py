import socket

def connect():
    try:
        userInput = input("Please enter a web address: ")
        host = userInput.split("/")[2]
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysock.connect((host, 80))
        cmd = "GET " + userInput + " HTTP/1.0\r\n\r\n"
        mysock.send(bytes(cmd, "utf8"))
        return mysock
    except:
        print("Please enter a valid URL\n\n")
        connect()

mysock = connect()

storedDocument = ""

while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    storedDocument += data.decode("utf8")

print(storedDocument[:3000])
print("\nThe document is " + str(len(storedDocument)) + " characters long\n")

mysock.close()