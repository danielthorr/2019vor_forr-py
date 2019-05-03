# Lokaverkefni

### Summary

The idea behind this project is that the client-side code is very light and only really does 3 things (`module: client.py`):
* Take in input from user
* Send input to server
* Receive and print output from server

The `server.py` module is very barebones as well. It mostly serves as a middle-man between the client and the `serverMethods.py` module, which handles all of the parsing and handling output.

All of the work is done by `serverMethods.py`, which handles all of the parsing and giving out the proper output.