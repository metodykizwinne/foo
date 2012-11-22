#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
import tkMessageBox
import psycopg2

from util import DBNAME, HOST

class LoginWindow:
    
    def __init__(self, master):

        master.title("Logowanie do systemu")
        
        self.frame = ttk.Frame(master, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Label(self.frame, text="Login:").grid(column=1, row=1, sticky=E)
        self.login = StringVar()
        self.login_entry = ttk.Entry(self.frame, textvariable=self.login)
        self.login_entry.grid(column=2, row=1, sticky=E)

        ttk.Label(self.frame, text="Hasło:").grid(column=1, row=2, sticky=E)
        self.password = StringVar()
        ttk.Entry(self.frame, show="*", textvariable=self.password).grid(column=2, row=2, sticky=E)

        ttk.Button(self.frame, text="Zaloguj", command=self.check_password).grid(column=2, row=3, sticky=(W, E))

        for child in self.frame.winfo_children(): child.grid_configure(padx=5, pady=5)
        
        self.login_entry.focus()
        master.bind('<Return>', self.check_password)

    def check_password(self, *args):
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DBNAME, self.login.get(), HOST, self.password.get()))
        except:                 # host może też być nieosiągalny
            tkMessageBox.showinfo("Błąd logowania", "Złe hasło/login!")
        
def main():    
    root = Tk()
    LoginWindow(root)
    root.mainloop()

main()
