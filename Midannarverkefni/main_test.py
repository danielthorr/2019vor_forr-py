from tkinter import *

def switch_frame(obj, frame_class):
    """Destroys current frame and replaces it with a new one."""
    new_frame = frame_class(obj)
    if obj._frame is not None:
        obj._frame.destroy()
    obj._frame = new_frame
    obj._frame.pack()

class StartPage(Frame):

    def __init__(self, width, height, master=None):
        Frame.__init__(self, master)
        self.width = width
        self.height = height
        self.master = master
        self.btnWidth = 10
        self.btnHeight = 4
        self.init_window()

    def init_window(self):

        self.master.title("Hangman")

        #Allow the widget to take the full space of the window
        self.pack(fill=BOTH, expand=1)
        btnStart = Button(self, text="Start", command=self.start)
        btnQuit = Button(self, text="Quit", command=self.client_exit)
        txt = Label(self, text="Want to play Hangman?")

        #btnStart.config(height=btnHeight, width=btnWidth)
        #btnStart.place(relx=0.5,y=0, anchor=CENTER)

        elements = [txt, btnStart, btnQuit]

        for i in range(len(elements)):
            if (i > 0):
                elements[i].config(width=self.btnWidth, height=self.btnHeight)
            elements[i].grid(row=(i+1), column=1, pady=15+(5*i))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        #Create a menu instance
    def dothing(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Quit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Undo")
        edit.add_command(label="Show Img")
        menu.add_cascade(label="Edit", menu=edit)


        quitButton = Button(self, text="Quit", command=self.client_exit)
        quitButton.place(x=0, y=0)

    def start(self):
        text = Label(self, text="Change state plz")
        text.pack()

    def client_exit(self):
        exit()    

class DifficultyPage(Frame):

    def __init__(self, width, height, master=None):
        Frame.__init__(self, master)
        self.width = width
        self.height = height
        self.master = master
        self.difficulty = "easy"
        self.btnWidth = 10
        self.btnHeight = 4
        self.startSettings()

    def startSettings(self):
        self.master.title("Hangman")
        self.pack(fill=BOTH, expand=1)
        
        difficulty = ["Easy", "Medium", "Hard"]
        btns = []
        Button(self, text="Easy", command=self.setDifficulty(0), width=self.btnWidth, height=self.btnHeight).grid(row=1, column=1)
        Button(self, text="Medium", command=self.setDifficulty(1), width=self.btnWidth, height=self.btnHeight).grid(row=2, column=1)
        Button(self, text="Hard", command=self.setDifficulty(2), width=self.btnWidth, height=self.btnHeight).grid(row=3, column=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def setDifficulty(self, diff):
        if (diff == 0):
            self.difficulty = "easy"
        elif (diff == 1):
            self.difficulty = "medium"
        elif (diff == 2):
            self.difficulty = "hard"
        else:
            print("Error setting difficulty")
            
        print(self.difficulty)

winWidth = 500
winHeight = 300
tk = Tk()
tk.geometry(str(winWidth) + "x" + str(winHeight))
app = DifficultyPage(winWidth, winHeight, tk)

tk.mainloop()

