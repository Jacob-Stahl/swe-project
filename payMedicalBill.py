
# Adding support for python 2 & 3

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    
import tkinter.messagebox
import os
import random
import string

# tkinter window
class App:
    def __init__(self, master):
        self.master = master

        # creating the format in master
        self.left = Frame(master, width=600, height=720, bg='lightblue')
        self.left.pack(side = LEFT)

        self.right = Frame(master, width=400, height=720, bg='steelblue')
        self.right.pack(side = RIGHT)

        self.heading = Label(self.left, text="Enter Payment Details", font=('arial 18'), fg='black', bg='lightblue')
        self.heading.place(x=160, y=50)

        # Payment Type

        self.gender = Label(self.left, text="Payment Type", font=('arial 12'), fg='black', bg='lightblue')
        self.gender.place(x=65, y=100)

        # cardNumber
        self.cardNumber = Label(self.left, text="Card Number", font=('arial 12'), fg='black', bg='lightblue')
        self.cardNumber.place(x=65, y=140)
        self.cardNumber = Entry(self.left, width=30)
        self.cardNumber.place(x=275, y=140)

        # NameOnCard
        self.NameOnCard = Label(self.left, text="Name on Card", font=('arial 12'), fg='black', bg='lightblue')
        self.NameOnCard.place(x=65, y=180)
        self.NameOnCard = Entry(self.left, width=30)
        self.NameOnCard.place(x=275, y=180)

        # paymentAmount
        self.paymentAmount = Label(self.left, text="Payment Amount", font=('arial 12'), fg='black', bg='lightblue')
        self.paymentAmount.place(x=65, y=220)
        self.paymentAmount = Entry(self.left, width=30)
        self.paymentAmount.place(x=275, y=220)

        # appointment date
        self.ExpirationDate = Label(self.left, text="Expiration Date", font=('arial 12'), fg='black', bg='lightblue')
        self.ExpirationDate.place(x=65, y=240)
        self.ExpirationDate = Entry(self.left, width=30)
        self.ExpirationDate.place(x=275, y=240)

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

        # button to perform a command
        self.submit = Button(self.left, text="Submit", width=20, height=2, bg='steelblue', command=self.generateReferenceNumber)
        self.submit.place(x=220, y=400)

    # function to call when the submit button is clicked
    def generateReferenceNumber(self):

        letters_and_digits = string.ascii_letters + string.digits
        referenceNumber = ''.join((random.choice(letters_and_digits) for i in range(32)))

        tkinter.messagebox.showinfo("Reference Number: ", referenceNumber)

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

root.bind('<Return>', b.generateReferenceNumber)

# end the loop
root.mainloop()