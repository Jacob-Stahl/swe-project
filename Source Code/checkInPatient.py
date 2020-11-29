# Adding support for python 2 & 3

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    
import tkinter.messagebox
import os, sys, webbrowser, time, random, string
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

        self.heading.place_forget()
        self.name.place_forget()
        self.namenet.place_forget()
        self.search.place_forget()

        self.heading = Label(self.master, text="Enter Additional Information",  fg='black', font=('lightblue'), bg='lightblue')
        self.heading.place(x=180, y=40)

        self.patientAddress = Label(self.master, text="Address", font=('arial 12'), fg='black')
        self.patientAddress.place(x=65, y=100)

        self.patientAddressEntry = Entry(self.master, width=30)
        self.patientAddressEntry.place(x=275, y=100)

        self.patientCity = Label(self.master, text="City", font=('arial 12'), fg='black')
        self.patientCity.place(x=65, y=140)

        self.patientCityEntry = Entry(self.master, width=30)
        self.patientCityEntry.place(x=275, y=140)

        self.patientState = Label(self.master, text="State", font=('arial 12'), fg='black')
        self.patientState.place(x=65, y=180)

        self.patientStateEntry = Entry(self.master, width=30)
        self.patientStateEntry.place(x=275, y=180)

        self.patientZip = Label(self.master, text="Zip", font=('arial 12'), fg='black')
        self.patientZip.place(x=65, y=220)

        self.patientZipEntry = Entry(self.master, width=30)
        self.patientZipEntry.place(x=275, y=220)

        self.patientEmail = Label(self.master, text="Patient Email", font=('arial 12'), fg='black')
        self.patientEmail.place(x=65, y=260)

        self.patientEmailEntry = Entry(self.master, width=30)
        self.patientEmailEntry.place(x=275, y=260)

        self.patientPhoneNumber = Label(self.master, text="Patient Phone Number", font=('arial 12'), fg='black')
        self.patientPhoneNumber.place(x=65, y=300)

        self.patientPhoneNumberEntry = Entry(self.master, width=30)
        self.patientPhoneNumberEntry.place(x=275, y=300)

        self.patientSSN = Label(self.master, text="Patient SSN", font=('arial 12'), fg='black')
        self.patientSSN.place(x=65, y=340)

        self.patientSSNEntry = Entry(self.master, width=30)
        self.patientSSNEntry.place(x=275, y=340)
        
        self.patientHealthInsurance = Label(self.master, text="Patient Health Insurance", font=('arial 12'), fg='black')
        self.patientHealthInsurance.place(x=65, y=380)

        self.patientHealthInsuranceEntry = Entry(self.master, width=30)
        self.patientHealthInsuranceEntry.place(x=275, y=380)

        self.submit = Button(self.master, text="Add Additional Information", width=20, height=2, bg='steelblue', command=self.addAdditionalAppointment)
        self.submit.place(x=220, y=500)

    def addAdditionalAppointment(self):

        # getting the user inputs
        self.val1 = self.namenet.get()
        self.val2 = self.patientAddressEntry.get()
        self.val3 = self.patientCityEntry.get()
        self.val4 = self.patientStateEntry.get()
        self.val5 = self.patientZipEntry.get()
        self.val6 = self.patientEmailEntry.get()
        self.val7 = self.patientPhoneNumberEntry.get()
        self.val8 = self.patientSSNEntry.get()
        self.val9 = self.patientHealthInsuranceEntry.get()

        print(self.val3, self.val9, self.val1)

        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '' or self.val6 == '' or self.val7 == '' or self.val8 == '' or self.val9 == '':
            tkinter.messagebox.showwarning("Warning","Please fill up all the fields")
        else:
            addPatientInfoResponse = addPatientInfo(self.val1, self.val2, self.val3, self.val4, self.val5, self.val7, self.val6, self.val8, self.val9)

            if addPatientInfoResponse:
                tkinter.messagebox.showinfo("Success", "additional information added!")

                self.heading.place_forget()
                self.patientAddress.place_forget()
                self.patientAddressEntry.place_forget()
                self.patientCity.place_forget()
                self.patientCityEntry.place_forget()
                self.patientState.place_forget()
                self.patientStateEntry.place_forget()
                self.patientZip.place_forget()
                self.patientZipEntry.place_forget()
                self.patientEmail.place_forget()
                self.patientEmailEntry.place_forget()
                self.patientPhoneNumber.place_forget()
                self.patientPhoneNumberEntry.place_forget()
                self.patientSSN.place_forget()
                self.patientSSNEntry.place_forget()
                self.patientHealthInsurance.place_forget()
                self.patientHealthInsuranceEntry.place_forget()
                self.submit.place_forget()

                self.heading = Label(self.master, text="Enter Payment Details", font=('arial 18'), fg='black')
                self.heading.place(x=160, y=50)

                # Payment Type

                self.paymentType = Label(self.master, text="Payment Type", font=('arial 12'), fg='black')
                self.paymentType.place(x=65, y=100)

                # cardNumber
                self.cardNumber = Label(self.master, text="Card Number", font=('arial 12'), fg='black')
                self.cardNumber.place(x=65, y=140)
                self.cardNumber = Entry(self.master, width=30)
                self.cardNumber.place(x=275, y=140)

                # NameOnCard
                self.NameOnCard = Label(self.master, text="Name on Card", font=('arial 12'), fg='black')
                self.NameOnCard.place(x=65, y=180)
                self.NameOnCard = Entry(self.master, width=30)
                self.NameOnCard.place(x=275, y=180)

                # paymentAmount
                self.paymentAmount = Label(self.master, text="Payment Amount", font=('arial 12'), fg='black')
                self.paymentAmount.place(x=65, y=220)
                self.paymentAmount = Entry(self.master, width=30)
                self.paymentAmount.place(x=275, y=220)

                # appointment date
                self.ExpirationDate = Label(self.master, text="Expiration Date", font=('arial 12'), fg='black')
                self.ExpirationDate.place(x=65, y=260)
                self.ExpirationDate = Entry(self.master, width=30)
                self.ExpirationDate.place(x=275, y=260)

                # gender list
                CardList = ["Debit", "Credit"]

                # Option menu
                self.var = tk.StringVar()
                self.var.set(CardList[0])

                self.opt = tk.OptionMenu(self.master, self.var, *CardList)
                self.opt.config(width=10, font=('arial', 11))
                self.opt.place(x=275, y=100)

                # callback method
                def callback(*args):
                    for i in range(len(CardList)):
                        if CardList[i] == self.var.get():
                            self.cardEntry = CardList[i]
                            break
                
                self.var.trace("w", callback)

                self.submit = Button(self.master, text="Pay Medical Bill", width=20, height=2, bg='steelblue', command=self.payMedicalBill)
                self.submit.place(x=220, y=400)
            else:
                tkinter.messagebox.showerror("Failed", "Additional Information cannot be added!")

    def payMedicalBill(self):

        letters_and_digits = string.ascii_letters + string.digits
        referenceNumber = ''.join((random.choice(letters_and_digits) for i in range(32)))
        paymentType = "debit" if self.cardEntry == 0 else "credit"
        self.receipt = """
            Patient ID: {}
            Name: {}
            Date: {}
            Amount: ${}
            Payment Type: {}
            Reference_Number:
            {}
        """.format(
            self.PatientID.get(),
            self.NameOnCard.get(),
            self.ExpirationDate.get(),
            self.paymentAmount.get(),
            paymentType,
            referenceNumber,
        )

        tkinter.messagebox.showinfo("Reciept and Reference number", self.receipt)

#creating the object
root = tk.Tk()
b = App(root)

# resolution of the window
root.geometry("600x600")

# preventing the resize feature
root.resizable(False, False)

# title of the window
root.title("Check In Patient")

# icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.search_db)

# end the loop
root.mainloop()