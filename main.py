#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
import tkMessageBox
import psycopg2

import core
from util import *

root = Tk()

class LoginWindow:
    
    def __init__(self):
        self.window = Toplevel(root)
        self.window.protocol("WM_DELETE_WINDOW", root.quit)
        self.window.title("Logowanie do systemu")
        
        self.frame = ttk.Frame(self.window, padding="3 3 12 12")
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
        self.window.bind('<Return>', self.check_password)

    def check_password(self, *args):
        try:
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DBNAME, self.login.get(), HOST, self.password.get()))
        except:                 # host może też być nieosiągalny
            tkMessageBox.showinfo("Błąd logowania", "Złe hasło/login!")

class CaseSelectionWindow:
    
    def __init__(self, conn, user):
        self.conn = conn
        self.user = user
        
        self.window = Toplevel(root)
        self.window.protocol("WM_DELETE_WINDOW", root.quit)
        self.window.title("Lista spraw")

        columns = ('Nr sprawy', 'Właściciel', 'Data otwarcia', 'Data zamknięcia')
        self.ctree = ttk.Treeview(self.window, columns=columns, show="headings")

        for col in columns:
            self.ctree.column(col, width=150)
            self.ctree.heading(col, text=col)

        cur = conn.cursor()
        cur.execute("SELECT Sprawa, Policjant, Data_otwarcia, Data_zamkniecia FROM sprawy")

        for (case, owner, creation_date, closure_date) in cur.fetchall():
            record_display = (case, owner, creation_date, closure_date if closure_date != None else "sprawa otwarta")
            self.ctree.insert('', 'end', values=record_display)
            
        self.ctree.grid(column=0, row=1, columnspan=2)

        ttk.Button(self.window, text="Otwórz").grid(column=0, row=0, sticky=W)
        ttk.Button(self.window, text="Utwórz nową sprawę", command=self.create_case).grid(column=1, row=0, sticky=W)

        for child in self.window.winfo_children(): child.grid_configure(padx=2, pady=2)

        self.window.columnconfigure(1, weight=1)
        
        cur.close()
        conn.close()

    def create_case(self, *args):
        # tu wyskakuje okno z pytaniem o zawartość pola Sprawa

        core.create_case(self.conn, case, self.user)

        # tu wyskakuje okno edycji sprawy
        
def main():    
    root.withdraw()
    CaseSelectionWindow(psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DBNAME, USER, HOST, PASSWORD)), 'P666')
    root.mainloop()

main()
