# Link to tutorial https://realpython.com/python-sockets/# tcp-sockets
# For more information about all of these methods see the "server-more_comments" file.

# Import socket to use TCP/IP methods
import socket
from random import randint

try:
    # hostName = socket.getfqdn() # <- didn't work for me at home, but works at school. Something about proxy maybe.
    hostName = socket.gethostbyname(socket.gethostname())
except socket.gaierror:
    print("Error getting host ip/name")

# Establish a port to be used on both the server and client
port = 9999

class PlayerManager:
    def __init__(self):
        self.message = "Have fun"

        self.easyWords = ["glass", "tree", "swing", "house", "bright", "clean", "trim", "glue"]
        self.mediumWords = ["leaves", "grinding", "battery", "studio", "salesman"]
        self.hardWords = ["lethargic", "aggrivated", "calculative", "salesperson", "transition"]

        self.wordToGuess = ""

        self.difficulty = -1
        self.wordLength = 99
        self.guesses = 0
        self.lives = 10
        self.correctLetters = 0
        self.lettersGuessed = []
        self.revealed = ""

    def setDifficulty(self, diff):
        if (diff == "easy"):
            self.difficulty = 0
            self.wordToGuess = self.easyWords[randint(0, len(self.easyWords)-1)]
        if (diff == "medium"):
            self.difficulty = 1
            self.wordToGuess = self.mediumWords[randint(0, len(self.mediumWords)-1)]
        if (diff == "hard"):
            self.difficulty = 2
            self.wordToGuess = self.hardWords[randint(0, len(self.hardWords)-1)]

        self.wordLength = len(self.wordToGuess)

        for i in range(len(self.wordToGuess)):
                self.revealed += " _ "

        print("difficulty is: " + str(self.difficulty))
        print("word to guess: " + self.wordToGuess)

    def wordUpdate(self, guess):
        self.revealed = ""
        for i in range(len(self.wordToGuess)):
            if self.wordToGuess[i] in self.lettersGuessed:
                self.revealed += self.wordToGuess[i]
            else:
                self.revealed += " _ "

    def guessCheck(self, guess):
        guess = guess.lower()
        cancel = False

        if len(guess) != 1:
            self.message = "Make sure to only write one letter"
            cancel = True

        if guess in self.lettersGuessed:
            self.message = "You've already guessed this letter"
            cancel = True

        if not cancel:
            if guess not in self.wordToGuess:
                self.lives -= 1
                self.message = guess + " is incorrect"
            else:
                self.message = guess + " is correct"
                for char in self.wordToGuess:
                    if guess == char:
                        self.correctLetters += 1
            self.lettersGuessed.append(guess)
            self.wordUpdate(guess)

            if self.correctLetters >= len(self.wordToGuess):
                self.message = "Congratulations! You won!"
            elif self.lives <= 0:
                self.message = "I'm sorry, you lost. The word was \"" + self.wordToGuess + "\""

        self.send(self.message)

    def send(self, msg):
        guessLettersSend = " "
        for letter in self.lettersGuessed:
            guessLettersSend += letter + ", "
        message = "update;" + msg + ":" + str(self.lives) + ":" + guessLettersSend + ":" + self.revealed
        conn.sendto(bytes(message, "utf8"), addr)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    # Empty string means that the socket is going to accept any connection
    serverSocket.bind(("", port))

    # We need to listen() to the socket to be able to accept new connections
    # A default backlog value is chosen if empty
    serverSocket.listen()

    conn, addr = serverSocket.accept()

    with conn:
        print("\nPC ", addr, " successfully connected.\n")
        player = PlayerManager()

        while True:
            # We receive data in bytes, decode them to the utf8 standard
            data = conn.recv(1024).decode("utf8")

            command, content = data.split(";")

            print(content)

            if command == "ready":
                print("Client ready")
                conn.sendto(bytes("If you see this it's working", "utf8"), addr)
                player.send("Have fun!")
            if command == "gameready":
                print("received stuff")
                conn.sendto(bytes("Received the stuff", "utf8"), addr)

            if command == "guess":
                print("checking guess")
                player.guessCheck(content)

            if command == "diff":
                print("received difficulty")
                player.setDifficulty(content)

            # The client sends this message if it's ready to disconnect
            if data == "disconnecting":
                print("client is disconnecting")
                # This break statements breaks our while loop which keeps the connection open
                break

#   --------    Extra information   --------    #
#   bind() is used to associate the socket with a specific network interface and port number.
#   The values passed to bind() depend on the address family of the socket. In this example, socket.AF_INET expects a 2-tuple: (host, port).
#   host can be a hostname, IP address, or empty string. If an IP address is used, it should be IPv4.1 27.0.0.1 is the loopback interface, so only processes on the host will be able to connect to the server. If you pass an empty string, the server will accept connections on all available IPv4 interfaces.
#   port should be an integer from 1-65535 (0 is reserved). It’s the TCP port number to accept connections on from clients. Some systems may require superuser privileges if the port is < 1024.