# -*- coding: utf-8 -*-
     
from Tkinter import *
 
 
class StartUpWindow:
 
    def __init__(self, master, numbers):
 
        frame = Frame(master)
        frame.pack()
 
        for e in numbers:
            self.makeButton(e,frame)
 
    def makeButton(self,number,frame):
        self.number = Button(frame, text="Sprawa nr " + str(number), fg="red",
        command = lambda: self.open_investigation(number))
        self.number.pack()
 
    def open_investigation(self,e):
        print 'Otworz okno sprawy %s.' % str(e)
 
 
root = Tk()
app = StartUpWindow(root, range(10))
root.mainloop()
