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

        # Creating labels

        self.patientID = Label(self.left, text="Patient's ID", font=('arial 12'), fg='black', bg='lightblue')
        self.patientID.place(x=65, y=100)
        self.patientIDEntry = Entry(self.left, width=30)
        self.patientIDEntry.place(x=350, y=100)

        self.AppointmentDate = Label(self.left, text="Appointment Date (YYYY-MM-DD)", font=('arial 12'), fg='black', bg='lightblue')
        self.AppointmentDate.place(x=65, y=140)
        self.AppointmentDateEntry = Entry(self.left, width=30)
        self.AppointmentDateEntry.place(x=350, y=140)

        self.reason_for_visit = Label(self.left, text="Reason for visit", font=('arial 12'), fg='black', bg='lightblue')
        self.reason_for_visit.place(x=65, y=180)
        self.reason_for_visit_ent = Entry(self.left, width=30)
        self.reason_for_visit_ent.place(x=350, y=180)

        self.weight = Label(self.left, text="Weight", font=('arial 12'), fg='black', bg='lightblue')
        self.weight.place(x=65, y=220)
        self.weight_ent = Entry(self.left, width=30)
        self.weight_ent.place(x=350, y=220)

        self.height = Label(self.left, text="Height", font=('arial 12'), fg='black', bg='lightblue')
        self.height.place(x=65, y=260)
        self.height_ent = Entry(self.left, width=30)
        self.height_ent.place(x=350, y=260)

        self.blood_pressure = Label(self.left, text="Blood Pressure", font=('arial 12'), fg='black', bg='lightblue')
        self.blood_pressure.place(x=65, y=300)
        self.blood_pressure_ent = Entry(self.left, width=30)
        self.blood_pressure_ent.place(x=350, y=300)

        # button to perform a command
        self.submit = Button(self.left, text="Add Patient Record", width=20, height=2, bg='steelblue', command=self.add_patient_record)
        self.submit.place(x=190, y=400)

    # Gets triggered when the submit button is clicked
    def add_patient_record(self):
        # getting the user inputs
        self.val1 = self.patientIDEntry.get()
        self.val2 = self.AppointmentDateEntry.get()
        self.val3 = self.reason_for_visit_ent.get()
        self.val4 = self.weight_ent.get()
        self.val5 = self.height_ent.get()
        self.val6 = self.blood_pressure_ent.get()

        # Checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '' or self.val6 == '':
            tkinter.messagebox.showwarning("Warning","Please fill up all the details")

        else:
            addRecord(self.val1, self.val2, self.val3, self.val4, self.val5, self.val6)            
            tkinter.messagebox.showinfo("Success", "Record for "+ str(self.val1)+" has been added")

# Creating the object
root = tk.Tk()
b = App(root)

# Resolution of the window
root.geometry("580x500")

# Preventing the resize feature
root.resizable(False, False)

# Title of the window
root.title("Add Record")

# Icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.add_patient_record)

# End the loop
root.mainloop()