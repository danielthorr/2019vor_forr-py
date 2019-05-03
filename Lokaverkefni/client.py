import socket as s
import os

hostName = s.gethostbyname(s.gethostname())
port = 9999


with s.socket(s.AF_INET, s.SOCK_STREAM) as clientSocket:

  clientSocket.connect((hostName, port))

  # Send "ready" to the server so it can send back the file list
  clientSocket.sendall(b"0;ready")

  # Let's clear the console before we begin
  if os.name == "nt":
    clear = lambda: os.system("cls")
  elif os.name == "posix":
    clear = lambda: os.system("clear")

  # We create a function which clears the terminal screen for us
  clear()

  # We use these values to determine the state. If start is false, we want to wait until the
  # user types in "start" on the start screen
  start = False
  # When the disconnect variable is flipped to True, we disconnect from the server
  disconnect = False

  while True:
    if disconnect:
      clientSocket.sendall(b"0;disconnecting")
      break
    
    data = clientSocket.recv(1024).decode("utf8")

    # Here we check if the server has sent the "00" message. If that's the case,
    # then the player has finished the game and it's time to disconnect
    if data[:2] == "00":
      disconnect = True
      data = data.strip("00;")

    # The retry flag is only sent by the server if the user is on the start screen
    # and types in something other than start.
    if data != "retry": 
      print("Game:\n" + data + "\n")

    # If the disconnect variable is not set to True, then we take in the user input
    # otherwise we set it to exit
    inp = input(">>> ") if not disconnect else "exit"

    # Strip whitepspaces from beginning and end and convert to lowercase
    inp = str.strip(str.lower(inp))

    # When we start the game, we clear the screen
    if inp == "start":
      start = True
      clear()
    # If the user wants to exit, we flip the disconnect variable to true 
    # and then start the loop from the beginning
    elif inp == "exit":
      disconnect = True
      continue

    # If the player is on the start screen and hasn't typed in "start", we just reload the screen
    if not start:
      clientSocket.sendall(b"00")
      clear()
      continue

    # We split the input based on spaces
    commands = inp.split(" ")
    # We count the length of the list, if it is a list. Otherwise the length is just 1 word
    l = len(commands) if isinstance(commands, list) else 1
    # If the length of the list is higher than 0 but less than 5,
    # then we loop through it and insert a semicomma between each command
    if 0 < l < 5:
      inp = str(l)
      for command in commands:
        inp += ";" + command
    else:
      inp = ";%s" % inp

    # Send the input to the server
    clientSocket.sendall(bytes(inp, "utf8"))