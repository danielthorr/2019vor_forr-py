# Multi-frame tkinter application v2.3
import tkinter as tk
import socket, threading
from random import randint

hostName = socket.gethostbyname(socket.gethostname())

port = 9999

class Hangman(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switchFrame(StartFrame)

    def Update(self, data):
        command, content = data.split(";")

    def sendDifficulty(self, diff):
        clientSocket.sendall(bytes("diff;"+diff, "utf8"))
        self.switchFrame(GameFrame)

    def sendGuess(self, guess):
        clientSocket.sendall(bytes("guess;"+guess, "utf8"))
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
        tk.Button(self, text="Easy", command=lambda: master.sendDifficulty("easy")).pack()
        tk.Button(self, text="Medium", command=lambda: master.sendDifficulty("medium")).pack()
        tk.Button(self, text="Hard", command=lambda: master.sendDifficulty("hard")).pack()
        tk.Button(self, text="Back to main menu", command=lambda: master.switchFrame(StartFrame)).pack()

class GameFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        try:
            data = clientSocket.recv(1024).decode("utf8")
            command, content = data.split(";")
            content = content.split(":")
        except:
            pass
            
        tk.Label(self, text="Welcome to hangman").grid(row=0)
        tk.Label(self, text=content[0]).grid(row=0, column=1)
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
            
        self.hman[ (10-int(content[1])) ].grid(row=1, column=0)
        
        tk.Label(self, text="Letters guessed: " + content[2]).grid(row=1, column=1)
        tk.Label(self, text="Word progress: " + content[3]).grid(row=2, column=1)

        self.e = tk.Entry(self)
        self.e.grid(row=3, column=0)

        tk.Button(self, text="Check", command=lambda: master.sendGuess(self.e.get())).grid(row=3, column=1)

        #tk.Label(image=photo).pack()
        
        #tk.Button(self, text="Return to start page", command=lambda: master.switchFrame(StartFrame)).grid(row=4)
        tk.Button(self, text="Return to start page", command=lambda: send("SomeText")).grid(row=4)

data = "default"
from sysconfig import sys
def receive():
    print("checking socket...")

    while True:
        try:
            data = clientSocket.recv(1024).decode("utf8")
            data = tk.StringVar
            #print("Client received: " + data)
        except OSError:
            break

def send(thingToSend):
    clientSocket.sendall(bytes(thingToSend, "utf8"))
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect((hostName, port))

    clientSocket.sendall(b"ready;")

    #receiveThread = threading.Thread(target=receive)
    #receiveThread.start()

    app = Hangman()
    app.mainloop()