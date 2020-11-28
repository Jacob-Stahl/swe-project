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
        self.name = Label(master, text="Enter Patient's ID", font=('arial 12'))
        self.name.place(x=70, y=100)

        # entry for the name
        self.namenet = Entry(master, width=30)
        self.namenet.place(x=300, y=100)

        # search button
        self.search = Button(master, text="Enter", width=12, height=1, bg='steelblue', command=self.search_db)
        self.search.place(x=230, y=150)
    
    # Searches the database
    def search_db(self):
        self.input = self.namenet.get()

        self.res = getAppointment(self.input)

        self.patient_name = self.res[0]
        self.patient_birthday = self.res[1]
        self.gender = self.res[2]
        self.docName = self.res[3]
        self.date = str(self.res[4])
        self.time = str(self.res[5])
        
        # creating the update form
        self.uname = Label(self.master, text="Patient's Name", font=('arial 12'))
        self.uname.place(x=70, y=220)

        self.uage = Label(self.master, text="Age", font=('arial 12'))
        self.uage.place(x=70, y=260)

        self.ulocation = Label(self.master, text="Doctor Name", font=('arial 12'))
        self.ulocation.place(x=70, y=340)

        self.utime = Label(self.master, text="Appointment Date (YYYY-MM-DD)", font=('arial 12'))
        self.utime.place(x=70, y=380)

        self.uphone = Label(self.master, text="Appointment Time (HH:MM)", font=('arial 12'))
        self.uphone.place(x=70, y=420)

        self.ent1 = Entry(self.master, width=30)
        self.ent1.place(x=300, y=220)
        self.ent1.insert(END, str(self.patient_name))

        self.ent2 = Entry(self.master, width=30)
        self.ent2.place(x=300, y=260)
        self.ent2.insert(END, str(self.patient_birthday))

        self.ent4 = Entry(self.master, width=30)
        self.ent4.place(x=300, y=340)
        self.ent4.insert(END, str(self.docName))

        self.ent5 = Entry(self.master, width=30)
        self.ent5.place(x=300, y=380)
        self.ent5.insert(END, str(self.date))

        self.ent6 = Entry(self.master, width=30)
        self.ent6.place(x=300, y=420)
        self.ent6.insert(END, str(self.time))

root = Tk()
b = App(root)
root.geometry("640x620")
root.resizable(False, False)
root.title("View Report")
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))
root.mainloop()