#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import psycopg2

from util import DBNAME, HOST

class LoginWindow:
    
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

        self.button = Button(frame, text="Zaloguj", fg="red", command=self.check_password)
        self.button.pack()

        self.password.bind('<Return>', self.check_password)

    def check_password(self, event=None):
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DBNAME, self.login.get(), HOST, self.password.get()))
        except:
            tkMessageBox.showinfo("Błąd logowania", "Złe hasło/login!")
        
def main():    
    root = Tk()
    LoginWindow(root)
    root.mainloop()

main()
