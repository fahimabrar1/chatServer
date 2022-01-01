# import all the required modules
from socket import *
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk

# import all functions /
# everthing from chat.py file
PORT = 5000
HOST = "127.0.0.1"
FORMAT = "utf-8"

#FORMAT = "utf-8"

# Create a new client socket
# and connect to the server
socket = socket(AF_INET,SOCK_STREAM)
socket.connect((HOST, PORT))


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):

        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.loginPanel = Toplevel()
        # set the title
        self.loginPanel.title("Login To Server")
        self.loginPanel.resizable(width=False,
                                 height=False)
        self.loginPanel.configure(width=400,
                                 height=400)
        # create a Label
        self.header = Label(self.loginPanel,
                            text="Please login to continue",
                            justify=CENTER,
                            font="Helvetica 14 bold")

        self.header.place(relheight=0.2,
                          relx=0.2)
        # create a Label
        self.name = Label(self.loginPanel,
                          text="Name: ",
                          font="Helvetica 12")

        self.name.place(relheight=0.4,
                        relx=0.1,
                        rely=0.2)

        # create a entry box for
        # tyoing the message
        self.nameField = Entry(self.loginPanel,
                               font="Helvetica 14")

        self.nameField.place(relwidth=0.5,
                             relheight=0.1,
                             relx=0.35,
                             rely=0.35)

        # set the focus of the curser
        self.nameField.focus()

        # create a Continue Button
        # along with action
        self.login_btn = Button(self.loginPanel,
                                text="LOGIN",
                                font="Helvetica 14 bold",
                                command=lambda: self.goAhead(self.nameField.get()))

        self.login_btn.place(relx=0.4,
                             rely=0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        self.loginPanel.destroy()
        self.OpenChatPanel(name)

        # the thread to receive messages
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    # The main layout of the chat
    def OpenChatPanel(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CLIENT CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=450,
                              height=550,
                              bg="#17202A")
        self.nameHeader = Label(self.Window,
                                bg="#17202A",
                                fg="#ffffff",
                                text=self.name,
                                font="Helvetica 13 bold",
                                pady=15)

        self.nameHeader.place(relwidth=1)


        self.textContainer = Text(self.Window,
                                  width=20,
                                  height=1,
                                  bg="#f5f5f5",
                                  fg="#383838",
                                  font="Helvetica 14",
                                  )

        self.textContainer.place(relheight=0.785,relwidth=.98,
                         rely=0.105 , relx=0.01)

        self.bottomContainer = Label(self.Window,
                                     bg="#ABB2B9",
                                     justify=CENTER,
                                     height=50)

        self.bottomContainer.place(relwidth=1,relheight=1 ,rely=.9 )

        self.InputField = Entry(self.bottomContainer,
                                bg="#ffffff",
                                fg="#383838",
                                font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.InputField.place(relwidth=0.74,
                              relheight=0.06,
                              rely=0.008,
                              relx=0.011)

        self.InputField.focus()

        # create a Send Button
        self.send_btn = Button(self.bottomContainer,
                               text="Send",
                               font="Helvetica 10 bold",
                               width=20,
                               bg="#17202A",
                               fg="#ffffff",
                               command=lambda: self.sendButton(self.InputField.get()))

        self.send_btn.place(relx=0.77,
                            rely=0.008,
                            relheight=0.06,
                            relwidth=0.22)

        self.textContainer.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textContainer)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textContainer.yview)

        self.textContainer.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textContainer.config(state=DISABLED)
        self.msg = msg
        self.InputField.delete(0, END)
        send_thread = threading.Thread(target=self.sendMessage)
        send_thread.start()

    # function to receive messages
    def receive(self):
        while True:
            try:
                message = socket.recv(1024).decode(FORMAT)


                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    socket.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textContainer.config(state=NORMAL)
                    self.textContainer.insert(END,
                                              message + "\n\n")

                    self.textContainer.config(state=DISABLED)
                    self.textContainer.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                socket.close()
                break

    # function to send messages
    def sendMessage(self):
        self.textContainer.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            socket.send(message.encode(FORMAT))
            break


# create a GUI class object
g = GUI()
