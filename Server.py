# import socket library
from socket import *

# import threading library
import threading

# Choose a port that is free
PORT = 5000
FORMAT = "utf-8"
# An IPv4 address is obtained
# for the server.
HOST = "127.0.0.1"


# the format in which encoding
# and decoding will occur
#FORMAT = "utf-8"

# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []

# Create a new socket for
# the server
socket = socket(AF_INET,
                       SOCK_STREAM)

# bind the address of the
# server to the socket
socket.bind((HOST, PORT))


# function to start the connection
def startChat():

    # listening for connections
    socket.listen()
    print("Listening To Connections...")

    while True:
        # accept connections and returns
        # a new connection to the client
        # and the address bound to it
        conn, addr = socket.accept()
        conn.send("NAME".encode(FORMAT))

        # 1024 represents the max amount
        # of data that can be received (bytes)
        name = conn.recv(1024).decode(FORMAT)

        # append the name and client
        # to the respective list
        names.append(name)
        clients.append(conn)

        print(f"Name is :{name}")

        # broadcast message
        broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))

        conn.send('Connection successful!'.encode(FORMAT))

        # Start the handling thread
        thread = threading.Thread(target=handle,
                                  args=(conn, addr))
        thread.start()

        # no. of clients connected
        # to the server
        print(f"active connections {threading.activeCount() - 1}")


# method to handle the
# incoming messages
def handle(conn, addr):
    print(f"new connection {addr}")
    connected = True

    while connected:
        # recieve message
        message = conn.recv(1024)
        print(message[0] , message[1])
        # broadcast message
        broadcastMessage(message)

    # close the connection
    conn.close()


# method for broadcasting
# messages to the each clients
def broadcastMessage(message):
    for client in clients:
        client.send(message)


# call the method to
# begin the communication
startChat()
