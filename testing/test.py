import tkinter as tk

class Window(tk.Frame):

    def __init__(self, width, height, master=None):
        super().__init__(master)
        self.width = width
        self.height = height
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        btn = {"width":10, "height":6}
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello world\nClick me!"
        self.hi_there["command"] = self.sayHi
        self.hi_there.pack(side="top")
        self.hi_there["geometry"](str(btn.width) + "x" + str(btn.height))
        self.quit = tk.Button(self, text="Quit", fg="red", command=root.destroy)

        self.quit.pack(side="bottom")

    def sayHi(self):
        print("Hey veretybody") 


root = tk.Tk()
app = Window(200, 140, root)
app.mainloop()