import os
import serverMethods
import socket as s

try:
  hostName = s.gethostbyname(s.gethostname())
except s.gaierror:
  print("Error getting host ip/name")

port = 9999

# Because we have a very short game we keep the start and intro in this module.

start = ("\t\tThe Devil Is In The Details\n"
          "\nThis is a text adventure game. You have to solve a few simple 'puzzles'."
          "\n\nThe commands are the following: \n|  turn  |  examine  |  use  |  inventory  |  help  |"
          "\nSome words need an extra specifier, such as 'use [item]' or 'examine [object]'"
          "\n\nIf you need a reminder of the keywords, write the 'help' command. It can also be used with other commands."
          "\nFor example 'help use' or 'help turn'"
          "\n\nType in start to begin. You can also type exit at any time to quit.")

intro= ("You open your eyes. 'Where am I?' you think to yourself. It's pitch black and you can't see a thing."
        "\nYou stand up, your back aching. The floor is made of concrete."
        "\nHow long have I been lying here?")
# input(">>> ")

# Create an instance of the GameManager object from the serverMethods module.
gm = serverMethods.GameManager()

with s.socket(s.AF_INET, s.SOCK_STREAM) as serverSocket:
  # Empty string means that the socket is going to accept any connection
  serverSocket.bind(("", port))

  # We need to listen() to the socket to be able to accept new connections
  # A default backlog value is chosen if empty
  serverSocket.listen()

  conn, addr = serverSocket.accept()

  with conn:
    print("\nPC ", addr, " successfully connected.\n")
      
    while True:
      data = conn.recv(1024).decode("utf8")
      # If the client sends "00", that means we should skip over it and let the client retry
      # If the client doesn't send "00", we split the data and grab the second item, which is the command
      command = "00" if data == "00" else data.split(";")[1]

      if command == "disconnecting":
        print("Client is disconnecting")
        break

      elif command in ["ready", "00"]:
        conn.sendto(bytes(start, "utf8"), addr)

      elif command == "start":
        conn.sendto(bytes(intro, "utf8"), addr)
        
      # We compare the command to the keywords we have in the GameManager instance
      elif command in gm.keyWords:
        # The GameManager instance sends back the appropriate response 
        # and the server sends it to the client
        sendString = gm.ParseCommand(data)
        conn.sendto(bytes(sendString, "utf8"), addr)
      else:
        conn.sendto(b"retry", addr)