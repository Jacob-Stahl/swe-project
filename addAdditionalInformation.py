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

        self.patientID = Label(self.left, text="patient's ID", font=('arial 12'), fg='black', bg='lightblue')
        self.patientID.place(x=65, y=100)

        self.patientIDEntry = Entry(master, width=30)
        self.patientIDEntry.place(x=275, y=100)

        self.patientAddress = Label(self.left, text="Address", font=('arial 12'), fg='black', bg='lightblue')
        self.patientAddress.place(x=65, y=140)

        self.patientAddressEntry = Entry(master, width=30)
        self.patientAddressEntry.place(x=275, y=140)

        self.patientCity = Label(self.left, text="City", font=('arial 12'), fg='black', bg='lightblue')
        self.patientCity.place(x=65, y=180)

        self.patientCityEntry = Entry(master, width=30)
        self.patientCityEntry.place(x=275, y=180)

        self.patientState = Label(self.left, text="State", font=('arial 12'), fg='black', bg='lightblue')
        self.patientState.place(x=65, y=220)

        self.patientStateEntry = Entry(master, width=30)
        self.patientStateEntry.place(x=275, y=220)

        self.patientZip = Label(self.left, text="Zip", font=('arial 12'), fg='black', bg='lightblue')
        self.patientZip.place(x=65, y=260)

        self.patientZipEntry = Entry(master, width=30)
        self.patientZipEntry.place(x=275, y=260)

        self.patientEmail = Label(self.left, text="Patient Email", font=('arial 12'), fg='black', bg='lightblue')
        self.patientEmail.place(x=65, y=300)

        self.patientEmailEntry = Entry(master, width=30)
        self.patientEmailEntry.place(x=275, y=340)

        self.patientPhoneNumber = Label(self.left, text="Patient Phone Number", font=('arial 12'), fg='black', bg='lightblue')
        self.patientPhoneNumber.place(x=65, y=340)

        self.patientPhoneNumberEntry = Entry(master, width=30)
        self.patientPhoneNumberEntry.place(x=275, y=300)

        self.patientSSN = Label(self.left, text="Patient SSN", font=('arial 12'), fg='black', bg='lightblue')
        self.patientSSN.place(x=65, y=380)

        self.patientSSNEntry = Entry(master, width=30)
        self.patientSSNEntry.place(x=275, y=380)
        
        self.patientHealthInsurance = Label(self.left, text="Patient Health Insurance", font=('arial 12'), fg='black', bg='lightblue')
        self.patientHealthInsurance.place(x=65, y=420)

        self.patientHealthInsuranceEntry = Entry(master, width=30)
        self.patientHealthInsuranceEntry.place(x=275, y=420)

        # button to perform a command
        self.submit = Button(self.left, text="Pay Medical Bill", width=20, height=2, bg='steelblue', command=self.addAdditionalAppointment)
        self.submit.place(x=220, y=460)

    # function to call when the submit button is clicked
    def addAdditionalAppointment(self):
        # getting the user inputs
        self.val1 = self.patientIDEntry.get()
        self.val2 = self.patientAddressEntry.get()
        self.val3 = self.patientCityEntry.get()
        self.val4 = self.patientStateEntry.get()
        self.val5 = self.patientZipEntry.get()
        self.val6 = self.patientEmailEntry.get()
        self.val7 = self.patientPhoneNumberEntry.get()
        self.val8 = self.patientSSNEntry.get()
        self.val9 = self.patientHealthInsuranceEntry.get()

        # checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '' or self.val6 == '' or self.val7 == '' or self.val8 == '' or self.val9 == '':
            tkinter.messagebox.showwarning("Warning","Please fill up all the fields")
        else:
            if addPatientInfo(self.val1, self.val2, self.val3, self.val4, self.val5, self.val7, self.val6, self.val8, self.val9):
                tkinter.messagebox.showinfo("Success, additional information added!")
                os.system("python payMedicalBill.py")
            else:
                tkinter.messagebox.showerror("Failed", "Additional Information cannot be added!")

#creating the object
root = tk.Tk()
b = App(root)

# resolution of the window
root.geometry("600x560")

# preventing the resize feature
root.resizable(False, False)

# title of the window
root.title("Add Additional Appointment")

# icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.addAdditionalAppointment)

# end the loop
root.mainloop()