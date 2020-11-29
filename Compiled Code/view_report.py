# Adding support for python 2 & 3

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk

import tkinter.messagebox
import os, sys
from PIL import Image, ImageTk
import random, string
from DBInterface import *

class App:
    def __init__(self, master):
        self.master = master
        
        # heading label
        self.heading = Label(master, text="View Report",  fg='black', font=('arial 18'))
        self.heading.place(x=180, y=40)

        # search by name 
        self.name = Label(master, text="Enter Doctor's Name", font=('arial 12'))
        self.name.place(x=70, y=100)
        self.namenet = Entry(master, width=30)
        self.namenet.place(x=300, y=100)

        self.date = Label(master, text="Enter Date", font=('arial 12'))
        self.date.place(x=70, y=140)
        self.datenet = Entry(master, width=30)
        self.datenet.place(x=300, y=140)

        # search button
        self.search = Button(master, text="Enter", width=12, height=1, bg='steelblue', command=self.search_db)
        self.search.place(x=230, y=180)
    
    # Searches the database
    def search_db(self):
        self.val1 = self.namenet.get()
        self.val2 = self.datenet.get()

        self.res = createReport(self.val1, self.val2)

        self.docName = self.res[0]
        self.docID = self.res[1]
        self.no_of_appointments = self.res[2]
        self.revenue_earned = self.res[3]
        
        # creating the update form
        self.uname = Label(self.master, text="Doctor's Name", font=('arial 12'))
        self.uname.place(x=70, y=220)

        self.ent1 = Entry(self.master, width=30)
        self.ent1.place(x=300, y=220)
        self.ent1.insert(END, str(self.docName))

        self.udocID = Label(self.master, text="Doctor's ID", font=('arial 12'))
        self.udocID.place(x=70, y=260)

        self.ent2 = Entry(self.master, width=30)
        self.ent2.place(x=300, y=260)
        self.ent2.insert(END, str(self.docID))

        self.uno_of_appointments = Label(self.master, text="No of Appointments", font=('arial 12'))
        self.uno_of_appointments.place(x=70, y=300)


        self.ent4 = Entry(self.master, width=30)
        self.ent4.place(x=300, y=300)
        self.ent4.insert(END, str(self.no_of_appointments))

        self.urevenue_earned = Label(self.master, text="Revenue Earned", font=('arial 12'))
        self.urevenue_earned.place(x=70, y=340)

        self.ent5 = Entry(self.master, width=30)
        self.ent5.place(x=300, y=340)
        self.ent5.insert(END, str(self.revenue_earned))

root = Tk()
b = App(root)
root.geometry("640x620")
root.resizable(False, False)
root.title("View Report")
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))
root.mainloop()