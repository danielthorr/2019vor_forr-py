import os
#120 40

class TextManager():
  
  def __init__(self):
    self.terminalSize = "120,40"
    self.SetTerminalSize()
    
  def SetTerminalSize(self):
    os.system(f"mode {self.terminalSize}")

class LevelManager():

  def __init__(self):
    self.currentLevel = 0
    
txtMan = TextManager()

input("press enter to exit")

'''

exit = False
while exit == False:
  choice = input("width;height or (e)xit")

  if choice == "e" or choice == "exit":
    break
  choice = choice.split(";")
  x, y = choice
  os.system(f"mode {x},{y}")

'''