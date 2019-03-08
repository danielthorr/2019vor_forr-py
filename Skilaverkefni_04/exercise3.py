import socket
from urllib import request as urlr, parse as urlp, error as urlerr

def connect():
    try:
        userInput = input("Please enter a web address: ")
        return urlr.urlopen(userInput)
    except:
        print("Please enter a valid URL\n\n")
        connect()

storedDocument = ""

fhand = connect()

for line in fhand:
    storedDocument += line.decode("utf8")

print(storedDocument[:3000])
print("\nThe document is " + str(len(storedDocument)) + " characters long\n")
