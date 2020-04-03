""" Script for TCP chat server - relays messages to all clients """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *

clients = {}
addresses = {}
control_bool = True

while control_bool:

    HOST = input("HOST:")
    PORT = input("PORT:")

    if not HOST:
        HOST = "127.0.0.1"
    else:
        HOST = str(HOST)

    if not PORT:
        PORT = 5000
    else:
        PORT = int(PORT)

    BUFSIZ = 1024
    try:
        ADDR = (HOST, PORT)
        SOCK = socket(AF_INET, SOCK_STREAM)
        SOCK.bind(ADDR)
        control_bool = False
    except: 
        print("Invalid Entry")


def accept_incoming_connections():
    while True:
        client, client_address = SOCK.accept()
        print("%s:%s has connected." % client_address)
        client.send("Welcome to Chatapp! ".encode("utf8"))
        client.send("Now type your name and press enter!".encode("utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()


def handle_client(conn, addr): 
    name = conn.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type #quit to exit.' % name
    conn.send(bytes(welcome, "utf8"))
    msg = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(addr[0], addr[1]))
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name
    while True:
        msg = conn.recv(BUFSIZ)
        if msg != bytes("#quit", "utf8"):
            broadcast(msg, name + ": ")
        else:
            conn.send(bytes("#quit", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SOCK.listen(5) 
    print("Chat Server has Started !!")
    print("Waiting for Connection...")

    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
  
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    
    SOCK.close()

