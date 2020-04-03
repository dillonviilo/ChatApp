""" Script for Tkinter GUI chat client. """

from tkinter import *
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import emoji

control_bool = True

def receive():
    while True:
        try:
            msg = sock.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, emoji.emojize(msg))
        except OSError: 
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    sock.send(bytes(msg, "utf8"))
    if msg == "#quit":
        sock.close()
        top.quit()

def on_closing(event=None):
    my_msg.set("#quit")
    send()

def smiley_button_tieup(event=None):
    my_msg.set(":grinning_face_with_big_eyes:")  
    send()

def sad_button_tieup(event=None):
    my_msg.set(":winking_face_with_tongue:")   
    send()

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
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(ADDR)
        control_bool = False
    except:
         print("Invalid Entry")

top = Tk()
top.title("ChatApp")
messages_frame = Frame(top)

my_msg = StringVar()
my_msg.set("")
scrollbar = Scrollbar(messages_frame)
msg_list = Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()

messages_frame.pack()

button_label = Label(top, text="Enter Message:")
button_label.pack()
entry_field = Entry(top, textvariable=my_msg, foreground="Red")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(top, text="Send", command=send)
send_button.pack()
smiley_button = Button(top, text=emoji.emojize(":grinning_face_with_big_eyes:"), command=smiley_button_tieup)
smiley_button.pack()
sad_button = Button(top, text=emoji.emojize(":winking_face_with_tongue:"), command=sad_button_tieup)
sad_button.pack()

quit_button = Button(top, text="Quit", command=on_closing)
quit_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive)
receive_thread.start()
mainloop() 