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
            user = self.login.get()
            password = self.password.get()
            conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DBNAME, user, HOST, password))
            self.window.destroy()
            CaseSelectionWindow(conn, user)
        except:                 # host może też być nieosiągalny
            tkMessageBox.showinfo("Błąd logowania", "Złe hasło/login!")

class CaseSelectionWindow:
    
    def __init__(self, conn, user):
        self.conn = conn
        self.user = user
        
        self.window = Toplevel(root)
        self.window.protocol("WM_DELETE_WINDOW", root.quit)
        self.window.title("Lista spraw")

        columns = ('Identyfikator sprawy', 'Właściciel', 'Data otwarcia', 'Data zamknięcia')
        self.ctree = ttk.Treeview(self.window, columns=columns, show="headings")

        for col in columns:
            self.ctree.column(col, width=150)
            self.ctree.heading(col, text=col, command=lambda col=col: self.treeview_sort_column(col, False))
 
        cases_to_list = core.cases_of_user(conn, user) + core.cases_user_can_access(conn, user)
        
        for list_entry in map(self.make_displayable, cases_to_list):
            self.ctree.insert('', '0', values=list_entry)
            
        self.ctree.grid(column=0, row=1, columnspan=2)

        ttk.Button(self.window, text="Otwórz").grid(column=0, row=0, sticky=W)
        ttk.Button(self.window, text="Utwórz nową sprawę", command=self.create_case).grid(column=1, row=0, sticky=W)

        for child in self.window.winfo_children(): child.grid_configure(padx=2, pady=2)

        self.window.columnconfigure(1, weight=1)
        
        conn.close()

    def treeview_sort_column(self, col, reverse):
        # znajdujemy odpowiednią kolejność wierszy
        l = [(self.ctree.set(k, col), k) for k in self.ctree.get_children('')]
        l.sort(reverse=reverse, key=lambda pair: pair[0])

        # przestawiamy
        for index, (val, k) in enumerate(l):
            self.ctree.move(k, '', index)

        # następnym razem sortujemy w odwrotnej kolejności
        self.ctree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def create_case(self, *args):
        # tu wyskakuje okno z pytaniem o zawartość pola Sprawa

        core.create_case(self.conn, case, self.user)

        # tu wyskakuje okno edycji sprawy

    # zamienia krotkę odpowiadającą sprawie na krotkę
    # nadającą się do wyświetlenia
    def make_displayable(self, case_info):
        (case, owner, creation_date, closure_date) = case_info
        return case_info if closure_date != None else (case, owner, creation_date, "sprawa otwarta")
        
def main():    
    root.withdraw()
    # LoginWindow()
    CaseSelectionWindow(psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (DBNAME, USER, HOST, PASSWORD)), 'pguser')
    root.mainloop()

main()
