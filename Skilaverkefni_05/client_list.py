import argparse
import json
import socket
import threading

# Here we receive incoming messages from clients and process them
def handle_client(client_list, conn, address):
    name = conn.recv(1024)
    name = name.decode("utf-8")
    # We create a dict with the name we received from the client, along with the client's ip and port
    entry = dict(zip(['name', 'address', 'port'], [name, address[0], address[1]]))
    # Then we insert the dict variable into the client_list dict using the name as the key
    client_list[name] = entry
    # Send back the client list and close the connection
    conn.sendall(bytes(json.dumps(client_list), "utf-8"))
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

# Launch the server
def server(client_list):
    print ("Starting server...")
    # Initializing all the appropriate socket options
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 5000))
    s.listen(5)
    # Listen to incoming connections
    while True:
        (conn, address) = s.accept()
        # When we receive an incoming connection we set the target of the thread to the handle_thread() function
        # we also send with it the empty client list, the client's socket object (conn) and the address bound to the socket
        t = threading.Thread(target=handle_client, args=(client_list, conn, address))
        # Setting daemon to true
        t.daemon = True
        # Starting the thread
        t.start()

# Launch the client
def client(name):
    # Initializing all the appropriate socket options
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 5000))
    s.send(bytes(name, "utf-8"))
    # Receive the server's response in a json format and print them out
    data = s.recv(1024)
    result = json.loads(data)
    print (json.dumps(result, indent=4))

# Parsing arguments from command line
def parse_arguments():
    # Initialize the ArgumentParser module
    parser = argparse.ArgumentParser()
    # Adding in arguments and storing them in our parser
    parser.add_argument('-c', dest='client', action='store_true')
    parser.add_argument('-n', dest='name', type=str, default='name')
    # Building arguments with parse_args()
    result = parser.parse_args()
    return result

def main():
    # Initialize client list as dict
    client_list = dict()
    # Fetch arguments from command line
    args = parse_arguments()
    # Checking if we should launch the client or the server
    if args.client:
        client(args.name)
    else:
        try:
            server(client_list)
        except KeyboardInterrupt:
            print ("Keyboard interrupt")

if __name__ == '__main__':
    main()