
# Adding support for python 2 & 3

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    
import tkinter.messagebox
import os, sys, webbrowser, time
from DBInterface import *

# tkinter window
class App:
    def __init__(self, master):
        self.master = master

        # heading label
        self.heading = Label(master, text="Check In Patient",  fg='black', font=('arial 18'))
        self.heading.place(x=180, y=40)

        # search criteria -->name 
        self.name = Label(master, text="Enter Patient's ID", font=('arial 12'))
        self.name.place(x=70, y=100)

        # entry for  the name
        self.namenet = Entry(master, width=30)
        self.namenet.place(x=300, y=100)

        # search button
        self.search = Button(master, text="Search", width=12, height=1, bg='steelblue', command=self.search_db)
        self.search.place(x=230, y=150)

    # function to call when the submit button is clicked
    def search_db(self):
        self.input = self.namenet.get()

        self.res = getAppointment(self.input)

        if self.res != None:
            os.system("python addAdditionalInformation.py")

#creating the object
root = tk.Tk()
b = App(root)

# resolution of the window
root.geometry("600x520")

# preventing the resize feature
root.resizable(False, False)

# title of the window
root.title("Check In Patient")

# icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.search_db)

# end the loop
root.mainloop()