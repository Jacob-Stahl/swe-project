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
        self.patientIDEntry.place(x=275, y=100)

        self.treatmentRecord = Label(self.left, text="Treatment Record", font=('arial 12'), fg='black', bg='lightblue')
        self.treatmentRecord.place(x=65, y=140)
        self.treatmentRecordEntry = Entry(self.left, width=30)
        self.treatmentRecordEntry.place(x=275, y=140)

        self.prescription = Label(self.left, text="Prescription", font=('arial 12'), fg='black', bg='lightblue')
        self.prescription.place(x=65, y=180)
        self.prescriptionEntry = Entry(self.left, width=30)
        self.prescriptionEntry.place(x=275, y=180)

        # button to perform a command
        self.submit = Button(self.left, text="Add Treatment", width=20, height=2, bg='steelblue', command=self.add_treatment)
        self.submit.place(x=190, y=400)

    # Gets triggered when the submit button is clicked
    def add_treatment(self):
        # getting the user inputs
        self.val1 = self.patientIDEntry.get()
        self.val2 = self.treatmentRecordEntry.get()
        self.val3 = self.prescriptionEntry.get()

        # Checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '':
            tkinter.messagebox.showwarning("Warning","Please fill up all the details")

        else:
            if addTreatment(self.val2, self.val3, self.val1):                
                tkinter.messagebox.showinfo("Success", "Treatment for "+ str(self.val1)+" has been added")
            else:
                tkinter.messagebox.showerror("Failed", "Treatment for "+ str(self.val1)+" cannot be added")

# Creating the object
root = tk.Tk()
b = App(root)

# Resolution of the window
root.geometry("580x500")

# Preventing the resize feature
root.resizable(False, False)

# Title of the window
root.title("Add Treatment")

# Icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.add_treatment)

# End the loop
root.mainloop()