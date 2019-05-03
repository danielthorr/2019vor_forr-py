# This object will handle all of the aspects of the game. Since the function of this class is
# not as important to the assignment, I will not go into detail on every if-else function.
class GameManager():

  def __init__(self):
    # These are the commands that the user has at their disposal
    self.keyWords = ["examine", "turn", "use", "help", "inventory"]
    self.rooms = ["north", # Here is the crowbar
    "east", # Here is the led light and lightswitch
    "south", # Here is the bag and it contains 5 stones
    "west" # Here is the box and when the box is opened with the crowbar there 4 candles inside
    ]
    # We start in the north room
    self.room = "north"
    # dict of the steps the user needs to take to progress
    self.progress = {"light": False, "box": False, "stonesPlaced": False, "candlesPlaced": False}
    # dict of the objects the user needs to find to progress
    self.playerItems = {"crowbar": False, "candles": False, "stones": False}
    # Here we would have a dict of booleans that we would use to notify the user of changes 
    # as they progress through the game
    self.notifications = {"allItems": False}
    # playerFocus always contains the second argument the user passes with a command
    # useItemWith is the fourth argument the user passes when they want to use an item with something else
    # Both of these are optional, commands can be used standalone but sometimes need to be combined
    self.playerFocus = ""
    self.useItemWith = ""

  # The turn method allows the player to rotate in place and face different walls
  def Turn(self, inp, args):
    l = len(args) if isinstance(args, list) else 1
    try:
      if args[0] in self.rooms:
        self.room = args[0]
        return "You turn to face the " + args[0] + " wall."
      elif l == 1 and args[0] in ["left", "right"]:
        if args[0] == "left":
          if self.room == "north":  self.room = "west"
          elif self.room == "north":  self.room = "west"
          elif self.room == "east":   self.room = "north"
          elif self.room == "south":  self.room = "east"
          elif self.room == "west":   self.room = "south"
        if args[0] == "right":
          if self.room == "north":  self.room = "east"
          elif self.room == "east":   self.room = "south"
          elif self.room == "south":  self.room = "west"
          elif self.room == "west":   self.room = "north"
        return "You turn to the " + args[0] + " and face the " + self.room + " wall."
    except IndexError:
      pass

  # Here are all the possible actions the user can take on the north wall
  def North(self, inp):
    if inp == "examine":
      if self.playerFocus == "crowbar" and not self.playerItems["crowbar"]: 
        return "It's a crowbar, big whoop"
      elif self.playerItems["crowbar"]: 
        return "There's nothing here, you took the crowbar"
      else: 
        return "You see a crowbar"

    elif inp == "use" and self.playerFocus == "crowbar" and not self.playerItems["crowbar"]:
        self.playerItems["crowbar"] = True
        return "You pick up the crowbar"

  # Here are all the possible actions the user can take on the east wall
  def East(self, inp):
    light = True if self.progress["light"] else False
    if inp == "examine":
      if self.playerFocus == "led":
        if light: return "You can hardly see the light coming from this LED with the lights turned on"
        else:     return "You feel around and find a switch of some sort"
      elif self.playerFocus in ["lightswitch", "switch"]:
        if light: return "You used this switch to turn on the lights. It's a light switch."
        else:     return "You can feel a switch of some sort, maybe you should try using it."
      else: 
          if light: return "You barely see a small LED and a switch that you used to turn on the lights"
          else:     return "You see a dim LED light on the wall"
    elif inp == "use":
      if self.playerFocus in ["lightswitch", "switch"]:
        if light: return "You already turned on the lights. You shouldn't turn them off or you won't see anything."
        else: 
          self.progress["light"] = True
          return "You turn on the light"
      elif self.playerFocus == "led":
        return "You can't do anything to the LED light"
  
  # Here are all the possible actions the user can take on the south wall
  def South(self, inp):
    if inp == "examine":
      if self.playerFocus == "bag" and not self.playerItems["stones"]: 
        return "It's a small linen bag tied together in a knot at the top."
      elif self.playerItems["stones"]: 
        return "There's nothing here, you took the bag of stones"
      else: 
        return "You see a small bag on the ground."

    elif inp == "use" and self.playerFocus == "bag" and not self.playerItems["stones"]:
      self.playerItems["stones"] = True
      return "You pick up the small bag and look inside. You find 5 stones, each with some sort of lettering or runes on it."

  # Here are all the possible actions the user can take on the west wall
  def West(self, inp):
    if inp == "examine":
      if self.playerFocus == "box":
        if self.progress["box"]: 
          if self.playerItems["candles"]: 
            return "There's a busted up box in here. You took the candles from it."
          else: return "You look inside the box and see 4 candles."
        else: return "It's a medium sized wooden box. More like a crate, really."
      elif self.progress["box"]: return "You see a wooden box, it's busted open."
      else: return "You see a wooden box, it doesn't look very sturdy"

    elif inp == "use":
      if self.playerFocus == "crowbar":
        if self.useItemWith == "box": 
          if self.progress["box"]: return "You already opened the box, what do you have against boxes?"
          else: 
            self.progress["box"] = True
            return "You bust open the box with your crowbar"
        else: return "What do you want to do with the crowbar?"
      elif self.playerFocus in ["box", "candles"]: 
        if self.progress["box"]: 
          if self.playerItems["candles"]: return "The box is empty, you already grabbed the candles."
          else:
            self.playerItems["candles"] = True
            return "You reach in and take the candles from the box."
        else: return "You may be strong and the box may be weak, but you're not strong enough to open the box with your bare hands."
      
  # Once the star appears, this option opens up. Here are all the possible actions the user can take on the star
  def Star(self, inp):
    if inp == "examine":
      if self.progress["stonesPlaced"] and self.progress["candlesPlaced"]: 
        return "It's a five-pointed star. You've laid the stones on each point and the candles between the points."
      elif self.progress["stonesPlaced"]: return "It's a five-pointed star. You've laid stones on each point."
      elif self.progress["candlesPlaced"]: return "It's a five-pointed star. You've laid candles between each of the points."
      else: return "In the middle of the room there's a ring on the floor with a five-pointed star."
    elif inp == "use":
      if self.playerFocus in ["candles", "stones"]:
        if self.useItemWith in ["star", "ring"]:
          if self.playerFocus == "candles": 
            self.progress["candlesPlaced"] = True
            return "You place each candle in an empty space between the points of the star."
          elif self.playerFocus == "stones": 
            self.progress["stonesPlaced"] = True
            return "You place a stone on each of the points of the star."
          else: return "You can't do that."

  # This method handles the help option and errors in user commands
  def CommandInfo(self, inp, intArg):
    if inp == "examine":
      if self.playerItems[self.playerFocus]:
        if self.playerFocus == "crowbar":
          return "It's a crowbar. You must know what a crowbar is."
        elif self.playerFocus == "stones":
          return "You have 5 small stones. Each one has some sort of rune or lettering on it."
        elif self.playerFocus == "candles":
          return "You have 4 candles. They are cylindrical and somewhere between 5 - 10 cm thick."
      else:
        return "Use examine on interactables like 'use [interactable]'. If you write examine without additional statements you will get information about the current location."
    elif inp == "inventory":
      returnString = ""
      for key, value in self.playerItems.items():
        if value: returnString += key + " "
      return returnString
    elif inp == "use":
      if self.useItemWith: return "Something went wrong. The correct syntax is 'use [item] with/on [interactable]'."
      elif self.playerFocus in self.playerItems: return "You need to specify what to use the item with. The correct syntax is 'use [item] with/on [interactable]'."
      else: return "You need to specify which item or interactable you want to use. Ex: 'use [item]' or 'use [interactable]'"
    elif inp == "turn":
      if intArg == 1: return "Turn where?\nEx: 'turn left/right' or 'turn north/east/south/west'"
      else: return "The proper way to use the 'turn' command is to write 'turn left/right' or 'turn north/east/south/west'\nExample: turn right | turn north"
    elif inp == "help":
      return ("These are the list of commands: | examine | use | turn | help |\n" +
        "Sometimes a command accepts more than one argument, for example: 'use [item]' or 'turn [direction]'")
    else: return "CommandInfo returned empty handed"

  # This method parses the user input and makes sure the right methods are run
  def ParseCommand(self, inp):
    # Convert the input to lowercase and strip whitespace from beginning and end
    inp = str.lower(str.strip(inp))
    # Command is a list of all the commands
    command = inp.split(";")
    # The first command is the number of commands, we copy it to the intArg variable
    intArg = int(command[0])
    # We set inp to be the first command (and the only one, if no others are passed by user)
    inp = command[1]
    # We copy all the extra commands starting at index 2 to commandArgs,
    # we use that list to set playerFocus and useItemWith
    commandArgs = command[2:]
    # We have to empty out the playerFocus and useItemWith variables every time
    self.playerFocus = ""
    self.useItemWith = ""

    # datastring will eventually be returned to the server module which gets sent to the user
    dataString = ""

    if intArg > 1:
      # If we have more than one arguments, we want the first of them to be the playerFocus
      self.playerFocus = commandArgs[0]
      # If we have more than 2 commands, it means the user wants to use an item with something else
      # So we check if the second argument is on or with, which is needed to use item on/with
      if intArg > 2 and commandArgs[1] in ["on", "with"]:
        self.useItemWith = commandArgs[2]

    # If the user is trying to interact with either the star or the ring and 
    # if the player has the necessary items
    if  (self.playerFocus in ["star", "ring"] 
    or self.useItemWith in ["ring", "circle"]
    and all(self.playerItems.values())):
      dataString = self.Star(inp)

    elif inp == "help":
      # If the user is typing help with another option, for example "help examine", 
      # then commandArgs[0] becomes the input that we need to pass to the CommandInfo method
      if intArg > 1: dataString = self.CommandInfo(commandArgs[0], intArg)
      else: dataString = self.CommandInfo(inp, intArg)
        
    elif inp == "turn":
      dataString = self.Turn(inp, commandArgs)

    # If the inp variable does not fit into any of the special cases above, we compare it to all the keywords
    elif inp in self.keyWords:

      # First we need to check if the light has been turned on because without it, the user can't see
      if not self.progress["light"]:
        if self.room == "east": dataString = self.East(inp)
        else: dataString = "You can't see anything. Try turning and examining your surroundings."
      
      # If the light is on, we simply check which wall the user is facing and run the corresponding method
      elif self.room == "north":  dataString = self.North(inp)
      elif self.room == "east":   dataString = self.East(inp)
      elif self.room == "south":  dataString = self.South(inp)
      elif self.room == "west":   dataString = self.West(inp)
        
    # If the datastring is empty, that means that none of the above resulted in any output.
    # That usually means that the user did not complete the command or there was another error
    if not dataString: 
      # We get the output from the CommandInfo method to indicate to the user what went wrong
      dataString = self.CommandInfo(inp, intArg)

    # If the player has all of the items and the allItems notification hasn't been shown, we send it out
    # This should only happen once; when the player has picked up the last item
    if all(self.playerItems.values()) and not self.notifications["allItems"]:
      self.notifications["allItems"] = True
      dataString += "\n\nSuddenly a ring appears on the floor in the middle of the room and in the ring appears a five-pointed star."
    # If the user has picked up all of the items and made all the progress, the game ends.
    # We send the end game output to the user
    elif all(self.playerItems.values()) and all(self.progress.values()):
      dataString += ("\n\nAll of a sudden the candles git lit. The star starts glowing red and in a puff of glitter, The Devil arises."
                      "\nThe Devil says to you: 'wazzap bra, let's get cronkd!'"
                      "\nBefore you know it, you're out partying with your best bro, The Devil.\n\n\t\tThe End.")
      # We pretend the number 00 to the string and the client will parse that as end-game and disconnect
      dataString = "00;"+dataString
      
    # Finally we return the string to the server, so it can be sent to the client
    return dataString