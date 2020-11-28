# Adding support for python 2 & 3

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    
import tkinter.messagebox
from DBInterface import *

# tkinter window
class App:
    def __init__(self, master):
        self.master = master

        # Creating the format in master
        self.left = Frame(master, width=600, height=720, bg='lightblue')
        self.left.pack(side = LEFT)

        # Heading
        self.heading = Label(self.left, text="Enter details", font=('arial 18'), fg='black', bg='lightblue')
        self.heading.place(x=220, y=50)

        # search by name 
        self.name = Label(master, text="Enter Patient's ID", font=('arial 12'))
        self.name.place(x=70, y=100)

        # entry for the name
        self.namenet = Entry(master, width=30)
        self.namenet.place(x=300, y=100)

        # search button
        self.search = Button(master, text="Search", width=12, height=1, bg='steelblue', command=self.search_db)
        self.search.place(x=230, y=150)

    def search_db(self):
        self.input = self.namenet.get()

        self.res = getRecord(self.input)

        self.patient_name = self.res[0]
        self.date = self.res[1]
        self.visit_reason = self.res[2]
        self.weight = self.res[3]
        self.height = self.res[4]
        self.blood_pressure = self.res[5]
        
        # creating the update form
        self.PatientID = Label(self.master, text="Patient's ID", font=('arial 12'))
        self.PatientID.place(x=70, y=220)
        self.ent1 = Entry(self.master, width=30)
        self.ent1.place(x=300, y=220)
        self.ent1.insert(END, str(self.patient_name))

        self.appointmentDate = Label(self.master, text="Appointment Date", font=('arial 12'))
        self.appointmentDate.place(x=70, y=260)
        self.ent2 = Entry(self.master, width=30)
        self.ent2.place(x=300, y=260)
        self.ent2.insert(END, str(self.date))

        self.visit_reason = Label(self.master, text="Reason for visit", font=('arial 12'))
        self.visit_reason.place(x=70, y=300)
        self.ent4 = Entry(self.master, width=30)
        self.ent4.place(x=300, y=340)
        self.ent4.insert(END, str(self.visit_reason))


        self.weight = Label(self.master, text="Weight", font=('arial 12'))
        self.weight.place(x=70, y=340)
        self.ent5 = Entry(self.master, width=30)
        self.ent5.place(x=300, y=380)
        self.ent5.insert(END, str(self.weight))

        self.height = Label(self.master, text="Height", font=('arial 12'))
        self.height.place(x=70, y=380)
        self.ent6 = Entry(self.master, width=30)
        self.ent6.place(x=300, y=420)
        self.ent6.insert(END, str(self.height))

        self.blood_pressure = Label(self.master, text="Blood Pressure", font=('arial 12'))
        self.blood_pressure.place(x=70, y=420)
        self.ent7 = Entry(self.master, width=30)
        self.ent7.place(x=300, y=460)
        self.ent7.insert(END, str(self.blood_pressure))

# Creating the object
root = tk.Tk()
b = App(root)

# Resolution of the window
root.geometry("580x500")

# Preventing the resize feature
root.resizable(False, False)

# Title of the window
root.title("Get Patient Record")

# Icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.search_db)

# End the loop
root.mainloop()