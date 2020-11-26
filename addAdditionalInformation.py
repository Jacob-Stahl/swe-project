# Adding support for python 2 & 3

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    
import tkinter.messagebox
import os, time

# tkinter window
class App:
    def __init__(self, master):
        self.master = master

        # creating the format in master
        self.left = Frame(master, width=600, height=720, bg='lightblue')
        self.left.pack(side = LEFT)

        self.right = Frame(master, width=400, height=720, bg='steelblue')
        self.right.pack(side = RIGHT)

        self.heading = Label(self.left, text="Enter Additional Details", font=('arial 18'), fg='black', bg='lightblue')
        self.heading.place(x=160, y=50)

        self.patientAddress = Label(self.left, text="Patient Address", font=('arial 12'), fg='black', bg='lightblue')
        self.patientAddress.place(x=65, y=100)

        self.patientAddressEntry = Entry(master, width=30)
        self.patientAddressEntry.place(x=275, y=100)

        self.patientEmail = Label(self.left, text="Patient Email", font=('arial 12'), fg='black', bg='lightblue')
        self.patientEmail.place(x=65, y=140)

        self.patientEmailEntry = Entry(master, width=30)
        self.patientEmailEntry.place(x=275, y=140)

        self.patientPhoneNumber = Label(self.left, text="Patient Phone Number", font=('arial 12'), fg='black', bg='lightblue')
        self.patientPhoneNumber.place(x=65, y=180)

        self.patientPhoneNumberEntry = Entry(master, width=30)
        self.patientPhoneNumberEntry.place(x=275, y=180)

        self.patientSSN = Label(self.left, text="Patient SSN", font=('arial 12'), fg='black', bg='lightblue')
        self.patientSSN.place(x=65, y=220)

        self.patientSSNEntry = Entry(master, width=30)
        self.patientSSNEntry.place(x=275, y=220)
        
        self.patientHealthInsurance = Label(self.left, text="Patient Health Insurance", font=('arial 12'), fg='black', bg='lightblue')
        self.patientHealthInsurance.place(x=65, y=260)

        self.patientHealthInsuranceEntry = Entry(master, width=30)
        self.patientHealthInsuranceEntry.place(x=275, y=260)

        # button to perform a command
        self.submit = Button(self.left, text="Pay Medical Bill", width=20, height=2, bg='steelblue', command=self.addAdditionalAppointment)
        self.submit.place(x=220, y=400)

    # function to call when the submit button is clicked
    def addAdditionalAppointment(self):
        # getting the user inputs
        self.val1 = self.patientAddressEntry.get()
        self.val2 = self.patientEmailEntry.get()
        self.val3 = self.patientPhoneNumberEntry.get()
        self.val4 = self.patientSSNEntry.get()
        self.val5 = self.patientHealthInsuranceEntry.get()

        # checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '':
            tkinter.messagebox.showwarning("Warning","Please fill up all the fields")
        else:
            tkinter.messagebox.showinfo("Success, additional information added!")
            time.sleep(10)
            os.system("python payMedicalBill.py")

#creating the object
root = tk.Tk()
b = App(root)

# resolution of the window
root.geometry("600x520")

# preventing the resize feature
root.resizable(False, False)

# title of the window
root.title("Add Additional Appointment")

# icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.addAdditionalAppointment)

# end the loop
root.mainloop()