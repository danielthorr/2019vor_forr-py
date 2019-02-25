# Multi-frame tkinter application v2.3
import tkinter as tk

class Hangman(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switchFrame(StartFrame)
        self.difficulty = -1

    def setDifficulty(self, diff):
        if (diff == "easy"):
            self.difficulty = 0
        if (diff == "medium"):
            self.difficulty = 1
        if (diff == "hard"):
            self.difficulty = 2

        self.switchFrame(GameFrame)

        print("difficulty is: " + str(self.difficulty))

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
        tk.Label(self, text="Welcome to hangman").pack(side="top", fill="x", pady=10)
        with open("hman1", "r") as file:
            tk.Label(self, image=tk.PhotoImage(file))
        
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switchFrame(StartPage)).pack()

if __name__ == "__main__":
    app = Hangman()
    app.mainloop()