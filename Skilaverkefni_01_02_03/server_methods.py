from pathlib import Path
import random

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

def CheckExtension(filename):
    # Checking the file extension
    if filename.lower()[-4:] != ".txt":
        filename += ".txt"
        print("User selected to receive: " + filename)

    return Path("archive") / filename, filename

# ---------------------

def Verkefni1(substate, filename):
    if substate == "0":
        return bytes("10;Select file:\n\nfile1.txt\nfile2.txt\nfile3.txt", "utf8")

    if substate == "1":
        print("Received answer from client")
        # Here we send the data variable to our function to check the client's answer and send back a filetmpPath = CheckExtension(message)
        tmpPath, fixedFileName = CheckExtension(filename)

        with open(tmpPath, "rb") as file:
            # Send the file to the client
            return bytes("12;filename:" + fixedFileName + "::content:", "utf8") + file.read()

def Verkefni2(substate, message):
    if substate == "0":
        return bytes("20;Please type the name of the file you would like to modify", "utf8")
    if substate == "1":
        pathToFile = Path("archive") / message
        if pathToFile.is_file():
            with open(pathToFile, "rb") as file:
                return bytes("21;" + message + "::", "utf8") + file.read()
        else:
            return bytes("23;would you like create the file (Y/N)?::" + message, "utf8")
    if substate == "2":
        filename, content = message.split("::")
        pathToFile = Path("archive") / filename
        if not pathToFile.is_file():
            return bytes("24;This file apparently doesn't exist", "utf8")
        else:
            with open(pathToFile, "w") as file:
                file.write(content)
            return bytes("24;File has been overwritten", "utf8")
    if substate == "3":
        filename, content = message.split("::")
        pathToCreate = Path("archive") / filename
        with open(pathToCreate, "w") as file:
            file.write(content)
        if pathToCreate.is_file():
            return bytes("24;File has successfully been created", "utf8")
        else:
            return bytes("24;Could not create file. Contact your local administrator or regular student", "utf8")

def Verkefni3(substate, message):
    if substate == "0":
        global hman
        hman = Hangman()
        return bytes("30;Welcome to hangman! Choose a difficulty level: easy, medium, hard", "utf8")
    if substate == "1":
        if message.lower() not in ["easy", "medium", "hard"]:
            return bytes("30;Something went wrong, please try again.")
        else:
            hman.InitWords(message)
            return bytes("32;" + hman.WriteToScreen(), "utf8")
    if substate == "2":
        if hman.correctLetters == len(hman.chosenWord):
            return bytes("32;|WOW YOU WIN! The word was [" + hman.chosenWord + "]", "utf8")
        elif hman.guessesLeft <= 0:
            return "32;|Oh man, you lost this one. The word was [" + hman.chosenWord + "]"
        #This will be our main loop for playing the game
        return bytes("32;" + hman.Guess(message), "utf8")

class Hangman:

    easyWords = ["glass", "tree", "swing", "house", "bright", "clean", "trim", "glue"]
    mediumWords = ["leaves", "grinding", "battery", "studio", "salesman"]
    hardWords = ["lethargic", "aggrivated", "calculative", "salesperson", "transition"]

    chosenWord = ""
    revealed = ""
    wordToScreen = ""

    correctLetters = 0
    guessesLeft = 0

    lettersGuessed = []

    def __init__(self):
        pass

    def InitWords(self, category):
        if category == "easy":
            self.chosenWord = self.easyWords[random.randint(0, len(self.easyWords)-1)]
            self.guessesLeft = 5
        if category == "medium":
            self.chosenWord = self.mediumWords[random.randint(0, len(self.mediumWords)-1)]
            self.guessesLeft = 8
        if category == "hard":
            self.chosenWord = self.hardWords[random.randint(0, len(self.hardWords)-1)]
            self.guessesLeft = 12

        for letter in self.chosenWord:
            self.wordToScreen += " _ "

        self.correctGuesses = 0

    def Guess(self, letter):
        if letter in self.lettersGuessed:
            return "\n[You already guessed this letter.]\n---------------------------" + self.WriteToScreen()
        if len(letter) == 1:
            if letter not in self.chosenWord:
                self.guessesLeft -= 1
            else:
                self.correctLetters += 1
            self.lettersGuessed.append(letter)
            self.WordUpdate(letter)
            printout = self.WriteToScreen()
            if self.correctLetters == len(self.chosenWord):
                return "|WOW YOU WIN! The word was [" + self.chosenWord + "]"
            elif self.guessesLeft <= 0:
                return "|Oh man, you lost this one. The word was [" + self.chosenWord + "]"
            return printout
        else:
            return "\n[Something went wrong, are you sure you only typed a single letter?]\n---------------------------" + self.WriteToScreen()


    def WordUpdate(self, letter):
        self.wordToScreen = ""
        for i in range(0,len(self.chosenWord)):
            if self.chosenWord[i] in self.lettersGuessed:
                self.wordToScreen += self.chosenWord[i]
            else:
                self.wordToScreen += " _ "

    def WriteToScreen(self):
        returnStr = "\n\nWords already guessed: [ "
        for letter in self.lettersGuessed:
            returnStr += letter + ", "
        returnStr += " ]"
        returnStr += "\nGuesses left: " + str(self.guessesLeft) + "\t|\tStatus: "
        for letter in self.wordToScreen:
            returnStr += letter
        returnStr += "\n\nWrite a letter here to guess: "
        return returnStr