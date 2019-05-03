class Player():
  def __init__(self):
    self.keyWords = ""

  def ParseInput(self, inp):
    # Strip whitespaces from the beginning and end and convert to lowercase
    inp = str.strip(str.lower(inp))
    l = str(len(inp))
    return l + ";" + inp