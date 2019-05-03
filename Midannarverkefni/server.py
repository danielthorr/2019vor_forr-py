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

# We create a class for our player and their values
class PlayerManager:
    def __init__(self):
        # Initiate some variables
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

        # If the player has won or lost the game is stopped
        self.stop = False

    # Get the player's preferred difficulty
    def setDifficulty(self, diff):
        if (diff == "easy"):
            self.wordToGuess = self.easyWords[randint(0, len(self.easyWords)-1)]
        if (diff == "medium"):
            self.wordToGuess = self.mediumWords[randint(0, len(self.mediumWords)-1)]
        if (diff == "hard"):
            self.wordToGuess = self.hardWords[randint(0, len(self.hardWords)-1)]

        # Here we fill a string with either blanks or the words
        # that the player has guessed correctly
        for i in range(len(self.wordToGuess)):
                self.revealed += " _ "

        print("difficulty is: " + str(self.difficulty))
        print("word to guess: " + self.wordToGuess)

    # This is used by the guessCheck method
    # to update the revealed word
    def wordUpdate(self, guess):
        self.revealed = ""
        for i in range(len(self.wordToGuess)):
            if self.wordToGuess[i] in self.lettersGuessed:
                self.revealed += self.wordToGuess[i]
            else:
                self.revealed += " _ "

    # Here we check what the player guessed
    def guessCheck(self, guess):
        # We assign it to lowercase so it doesn't become an issue
        guess = guess.lower()
        # Cancel is used to check if the player wrote
        # too many letters or has guessed the letter
        cancel = False
        # We wrap everything in one if statement that will not
        # run if the player has either won or lost
        if not self.stop:
            # If the player put too few or too many characters
            if len(guess) != 1:
                self.message = "Make sure to only write one letter"
                cancel = True

            # If the player has already guessed the letter
            if guess in self.lettersGuessed:
                self.message = "You've already guessed this letter"
                cancel = True

            if not cancel:
                # Check if the guess was correct and either
                # withdraw a life point or add 1 to correct guesses
                if guess not in self.wordToGuess:
                    self.lives -= 1
                    self.message = guess + " is incorrect"
                else:
                    self.message = guess + " is correct"
                    for char in self.wordToGuess:
                        if guess == char:
                            self.correctLetters += 1

                # Append the guessed letter to the list of letters guessed
                self.lettersGuessed.append(guess)
                # Update the revealed word to reflect the progress made
                self.wordUpdate(guess)

                # If the number of correct letters is the same or higher
                # than the word to guess, the player has won
                if self.correctLetters >= len(self.wordToGuess):
                    self.stop = True
                    self.message = "Congratulations! You won!"
                # If the player has run out of lives they have lost
                elif self.lives <= 0:
                    self.stop = True
                    self.message = "I'm sorry, you lost. The word was \"" + self.wordToGuess + "\""
        
        # When we've done all of our checking we call our send method
        # to send the results to our player
        self.send(self.message)

    # Here we send the player their updated progress
    def send(self, msg):
        # Create a string to send all the letters that the player has guessed so far
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

            # We split the data into command and content
            # We use the command to determine what step to take
            command, content = data.split(";")

            if command == "ready":
                print("Client ready")
                conn.sendto(bytes("If you see this it's working", "utf8"), addr)
                player.send("Have fun!")

            if command == "guess":
                print("checking guess")
                player.guessCheck(content)

            if command == "difficulty":
                print("received difficulty")
                player.setDifficulty(content)

            # The client sends this message if it's ready to disconnect
            if command == "disconnecting":
                print("client is disconnecting")
                # This break statements breaks our while loop which keeps the connection open
                break
