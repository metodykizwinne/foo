# -*- coding: utf-8 -*-

from Tkinter import *

class App:


    
    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.loginLabel = Label(frame, text="Login", fg="red")
        self.loginLabel.pack()
        self.login = Entry(frame)
        self.login.pack()

        self.passwordLabel = Label(frame, text="Hasło", fg="red")
        self.passwordLabel.pack()
        self.password = Entry(frame, show="*")
        self.password.pack()
        
        

        



        self.button = Button(frame, text="Zaloguj", fg="red", command=check_password)
        self.button.pack()


    def say_hi(self):
        print "hi there, everyone!"

root = Tk()

app = App(root)

root.mainloop()
