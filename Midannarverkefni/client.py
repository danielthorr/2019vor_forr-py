# Multi-frame tkinter application v2.3
import tkinter as tk
import socket, threading
from random import randint

hostName = socket.gethostbyname(socket.gethostname())

port = 9999

# The hangman class mostly serves to send to the server and to switch frames
class Hangman(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switchFrame(StartFrame)

    # All these different send commands just take in a value from our GameFrame class
    # and forward them to the server
    def sendDifficulty(self, diff):
        clientSocket.sendall(bytes("difficulty;"+diff, "utf8"))
        self.switchFrame(GameFrame)

    def sendGuess(self, guess):
        clientSocket.sendall(bytes("guess;"+guess, "utf8"))
        self.switchFrame(GameFrame)

    # This method switches frames to and from the start menu, options and game
    def switchFrame(self, frameClass):
        # Destroys current frame and replaces it with a new one.
        newFrame = frameClass(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = newFrame
        self.frame.pack()
    
    # This method simply sends a disconnect message to the server
    # then destroys itself
    def exitGame(self):
        clientSocket.sendall(b"disconnecting;")
        self.destroy()

# Start frame presents you with two buttons, very simple
class StartFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Start", command=lambda: master.switchFrame(SetupFrame)).pack()
        tk.Button(self, text="Quit", command=lambda: master.exitGame()).pack()

# The setupframe class gives us options for the difficulty setting
class SetupFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Let's play hangman, choose a difficulty").pack(side="top", fill="x", pady=10)

        # These next three buttons trigger the Hangman class' sendDifficulty method
        tk.Button(self, text="Easy", command=lambda: master.sendDifficulty("easy")).pack()
        tk.Button(self, text="Medium", command=lambda: master.sendDifficulty("medium")).pack()
        tk.Button(self, text="Hard", command=lambda: master.sendDifficulty("hard")).pack()

        # This button simply goes back to the main menu
        tk.Button(self, text="Back to main menu", command=lambda: master.switchFrame(StartFrame)).pack()

# The gameframe class is our main class, it displays everything we need to know during play
class GameFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Here we get data from our server and split it into usable chunks
        data = clientSocket.recv(1024).decode("utf8")
        # The command part, seperated by a semicomma is unused in this case
        command, content = data.split(";")
        # The content part is split into a list of messages
        content = content.split(":")
        
        tk.Label(self, text="Welcome to hangman").grid(row=0)

        # Here we use display the main message the game sends to us
        # those are things such as victory or failure and more
        tk.Label(self, text=content[0]).grid(row=0, column=1)

        # We have a list of names that we will use to show
        # the status of our hanging man
        self.images = [
            "hman0", "hman1", "hman2", "hman3", 
            "hman4", "hman5", "hman6", "hman7", 
            "hman8", "hman9", "hman10"
            ]
        # Instantiate a list
        self.hman = []
        # We iterate through the images in our images list
        # and load them into our hman list
        for i in range(len(self.images)):
            img = tk.PhotoImage(file=self.images[i] + ".png")
            self.hman.append(tk.Label(self, image=img))
            self.hman[i].image = img
            
        # We check how many lives we have left (content[1]) to
        # see which image we should display
        self.hman[ (10-int(content[1])) ].grid(row=1, column=0)
        
        # Display the letters the player has already guessed
        tk.Label(self, text="Letters guessed: " + content[2]).grid(row=1, column=1)
        # Display the progress of the word to be guessed
        tk.Label(self, text="Word progress: " + content[3]).grid(row=2, column=1)

        # Here we get input from the player
        self.e = tk.Entry(self)
        self.e.grid(row=3, column=0)

        # With the check button we trigger Hangman class' method sendGuess, 
        # passing in the player's guess
        tk.Button(self, text="Check", command=lambda: master.sendGuess(self.e.get())).grid(row=3, column=1)
        
# Open a socket to communicate with our server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    # Try to connect
    clientSocket.connect((hostName, port))

    # Send a message to confirm that we are ready
    clientSocket.sendall(b"ready;")

    # Activate the tkinter loop
    app = Hangman()
    app.mainloop()