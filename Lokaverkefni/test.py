import PySimpleGUI as psgui
import re

output = psgui.Multiline("Here is the large text thing", size=(70,20) )
suggest = psgui.Multiline("I might use this for 'autocorrect'", size=(54,1), font=("Arial", 12, "bold"), text_color="green" )
columnLeft = [[output], [suggest], [psgui.InputText("Type something here", size=(70,1), key="userInput", focus=True )]]
#columnRight = [[psgui.Input(do_not_clear=True, size=(35,1), enable_events=True)], [psgui.Button("Read"), psgui.Exit()]]
map = psgui.Canvas(canvas=None,
       background_color="Blue", 
       size=(200, 300),
       key="canvas", 
       tooltip="Map")
#layout = [[psgui.Column(columnLeft)], [psgui.Column(columnRight)]]
layout = [[psgui.Column(columnLeft), map]]
window = psgui.Window('Test', return_keyboard_events=True, background_color=None, use_default_focus=False,).Layout(layout).Finalize()
canv = window.FindElement("canvas").TKCanvas

intro= ("You open your eyes. 'Where am I?' you think to yourself. "
        "It's hard to see, the only light source is coming from a small hole "
        "in the roof. You stand up, your back aching. The floor is made of concrete "
        "How long have I been lying here?")
keyWords = ["examine", "go", "look", "use", "walk"]
wordPairs = { "look": "at", "go": "to", "walk": ["back", "to"] }
def Suggestions(uInp, empty=False):
  suggestWord = "| "
  l = len(uInp)
  if empty:
    for word in keyWords: 
      suggestWord += word + " | "
    suggest.Update(suggestWord)
    return
  for word in keyWords:
    if (len(uInp.split(" ")) == 2 or word == uInp) and word in wordPairs:
      first = ""
      if word != uInp:
        first = uInp.split(" ")[0]
      if word == uInp or word == first:
        if isinstance(wordPairs[word], list):
          for w in wordPairs[word]:
            suggestWord += w + " | "
        else:
          suggestWord += wordPairs[word] + " | "
    elif word[:l] == uInp:
      suggestWord += word + " | "
  suggest.Update(suggestWord)

inp = ""
lastInp = ""
txt1 = (intro, "text_color=blue")

def Output(text):
  tmpText = ">>> " + text + "\n\n"
  output.Update(tmpText)

while True:
  Output(intro)
  Output(intro)
  event, values = window.Read()
  if event == None or event == "Exit":
    break
  inp = str.strip(str.lower(values["userInput"]))
  #print(event, values)
  if inp != lastInp:
    Suggestions(inp)
  elif inp == "":
    Suggestions(inp, True)
  if re.search("[a-zA-Z]", event[0]) is None and event != " ":
    columnLeft[0][0].Update(values["userInput"])
  lastInp = inp

window.Close()