# Multi-frame tkinter application v2.3
import tkinter as tk
from random import randint

class Hangman(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switchFrame(StartFrame)

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

        self.switchFrame(GameFrame)

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

        self.switchFrame(GameFrame)

    def switchFrame(self, frameClass):
        # Destroys current frame and replaces it with a new one.
        newFrame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = newFrame
        self.frame.pack()
    
    def exitGame(self):
        self.destroy()

class StartFrame(tk.Frame):
    def __init__(self, master):
        self.width = 400
        self.height = 2505
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Start", command=lambda: master.switchFrame(SetupFrame)).pack()
        tk.Button(self, text="Quit", command=lambda: master.exitGame()).pack()

class SetupFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Let's play hangman, choose a difficulty").pack(side="top", fill="x", pady=10)
        #tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Easy", command=lambda: master.setDifficulty("easy")).pack()
        tk.Button(self, text="Medium", command=lambda: master.setDifficulty("medium")).pack()
        tk.Button(self, text="Hard", command=lambda: master.setDifficulty("hard")).pack()
        tk.Button(self, text="Back to main menu", command=lambda: master.switchFrame(StartFrame)).pack()

class GameFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome to hangman").grid(row=0)
        tk.Label(self, text=self.master.message).grid(row=0, column=1)
        self.images = [
            "hman0", "hman1", "hman2", "hman3", 
            "hman4", "hman5", "hman6", "hman7", 
            "hman8", "hman9", "hman10"
            ]
        self.hman = []
        for i in range(len(self.images)):
            img = tk.PhotoImage(file=self.images[i] + ".png")
            self.hman.append(tk.Label(self, image=img))
            self.hman[i].image = img
            
        self.hman[ (10-self.master.lives) ].grid(row=1, column=0)

        lettersGuessed = ""
        for letter in self.master.lettersGuessed:
            lettersGuessed += letter + ", "
        tk.Label(self, text="Letters guessed: " + lettersGuessed).grid(row=1, column=1)
        tk.Label(self, text="Word progress: " + self.master.revealed).grid(row=2, column=1)

        self.e = tk.Entry(self)
        self.e.grid(row=3, column=0)

        tk.Button(self, text="Check", command=lambda: master.guessCheck(self.e.get())).grid(row=3, column=1)

        #tk.Label(image=photo).pack()
        
        tk.Button(self, text="Return to start page", command=lambda: master.switchFrame(StartFrame)).grid(row=4)


if __name__ == "__main__":
    app = Hangman()
    app.mainloop()