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
from user_login import loginUser

from PIL import Image
from tkinter import ttk
import smtplib, random, string, socket
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class App:
    def __init__(self, master):
        self.master = master

        # menu bar
        Chooser = Menu()

        Chooser.add_command(label='Exit', command=lambda: exitRoot(root))

        root.config(menu=Chooser)
        
        self.loginLabel = Label(text="\nEnter login credentials\n", font=('arial 14 bold'), fg='black')
        self.loginLabel.pack()

        # login ID
        self.login_id = Label(text="Login ID*", font=('arial 12'), fg='black')
        self.login_id.place(x=60, y=70)

        # password
        self.password = Label(text="Password*", font=('arial 12'), fg='black')
        self.password.place(x=60, y=120)

        # entries for labels
        self.login_id_ent = Entry(width=20)
        self.login_id_ent.place(x=280, y=72)

        self.password_ent = Entry(width=20, show='*')
        self.password_ent.place(x=280, y=122)

        # button to login
        self.loginShield = PhotoImage(file = "resources/user-shield-100.png")
        self.buttonImage = self.loginShield.subsample(3, 3)
        self.submit = Button(text = 'Login', image=self.buttonImage, compound=LEFT, width=120, height=40, bg='steelblue', command=self.loginInterface)
        self.submit.place(x=170, y=200)

    # function to login
    def loginInterface(self):
        self.id = self.login_id_ent.get()
        self.password = self.password_ent.get()
        
        if self.id=="" or self.password=="":
            tkinter.messagebox.showwarning("All credentials required","Please enter all fields. Fields marked (*) are required.")
        else:
            self.login_id_ent.delete(0, END)
            self.password_ent.delete(0, END)

            currentUser = loginUser( str(self.id), self.password)

            if currentUser == "PW":
                tkinter.messagebox.showerror("Login Unsuccessful", "Password Incorrect! Please login again")

            elif currentUser == "USR":
                tkinter.messagebox.showerror("Login Unsuccessful", "Username not found! Please login again")

            else:
                self.db_name = currentUser.name
                self.db_pass = currentUser.employee_id
                self.db_designation = currentUser.classification
                tkinter.messagebox.showinfo("Login Successful", "Hello "+ self.db_name + "! You have successfully logged in as " + self.db_designation.capitalize())
                self.drawWin()

    #function to draw toplevel window
    def drawWin(self):
        # hiding root window
        hide_root()

        # drawing toplevel window
        top = Toplevel() 
        top.geometry("480x320+360+180") 
        top.title("Welcome") 
        
        # menu bar
        Chooser = Menu()
        itemone = Menu()

        if self.db_designation == 'clerk':
            Chooser.add_command(label='Add Appointment', command=self.appointment)
            Chooser.add_command(label='Edit Appointment', command=self.update)
            Chooser.add_command(label='Delete Appointment', command=self.delete)
            Chooser.add_command(label='View Appointment', command=self.display)
            Chooser.add_command(label='Check-In Patient', command=self.checkInPatient)

        elif self.db_designation == 'doctor':
            Chooser.add_command(label='View Appointment', command=self.display)
            Chooser.add_command(label='View Patient Measurements', command=self.getRecord)
            Chooser.add_command(label='Add Treatment', command=self.addTreatment)
        
        elif self.db_designation == 'nurse':
            Chooser.add_command(label='Update Measurements', command=self.addRecords)
        
        elif self.db_designation == 'ceo':
            Chooser.add_command(label='View Report', command=self.view_report)
        
        Chooser.add_command(label='Logout', command=lambda: self.logout(top))

        top.config(menu=Chooser)
        top.iconphoto(False, tk.PhotoImage(file="resources/icon.png"))

        self.left = Frame(top, width=130, height=130, bd=1, relief=RAISED)
        self.left.place(x=5, y=5)

        self.right = Frame(top, width=320, height=150)
        self.right.place(x=150, y=5)

        self.footer = Frame(top, width=480, height=30, bd=1, relief=RAISED, \
            highlightbackground="black", highlightthickness=1)
        self.footer.place(x=0, y=290)

        self.timeLabel = Label(self.footer, text="Logged in at "+time.strftime("%I:%M:%S %p"), font=('arial 10'), fg='black')
        self.timeLabel.place(x=5, y=3)
        
        self.userlogin = Label(self.right, text="You are logged in as:", font=('arial 12 bold'), fg='black')
        self.userlogin.place(x=5, y=20)

        self.Name = Label(self.right, text="Name: " + self.db_name, font=('arial 12'), fg='black')
        self.Name.place(x=5, y=50)

        self.Name = Label(self.right, text="Designation: " + self.db_designation.capitalize(), font=('arial 12'), fg='black')
        self.Name.place(x=5, y=80)

    def destroyTop(self, top):
        top.destroy()

    # function to close the top window
    def logout(self, top):
        MsgBox = tk.messagebox.askquestion('Logout Application','Are you sure you want to logout?', icon='warning')
        if MsgBox == 'yes':
            self.destroyTop(top)
            show_root()
  
    def appointment(self):
        os.system("python appointment.py")

    def update(self):
        os.system("python update.py")

    def display(self):
        os.system("python display.py")

    def delete(self):
        os.system("python delete.py")

    def addTreatment(self):
        os.system("python addTreatment.py")

    def view_report(self):
        os.system("python view_report.py")

    def checkInPatient(self):
        os.system("python checkInPatient.py")

    def addRecords(self):
        os.system("python addRecord.py")

    def getRecord(self):
        os.system("python getRecord.py")

root = tk.Tk()
b = App(root)
root.geometry("540x380+360+180")
root.resizable(False, False)
root.title("Hospital Managemnet Appointment Application - Login Window")
root.iconphoto(False, tk.PhotoImage(file="resources/icon.png"))
root.bind('<Return>', b.loginInterface)

def hide_root():
    # Hide root window
    root.withdraw()

def show_root():
    # Show root window
    root.deiconify()

def exitRoot(root):
    MsgBox = tk.messagebox.askquestion('Exit Application','Do you really want to exit?', icon='warning')
    if MsgBox == 'yes':
        root.destroy()

def updateStatusLabel(self):
    if(is_connected(self)):
        # set connected
        print("Status: Connected")
        self.netStatus.configure(text='Internet: Connected', fg='green')
        # self.Sub_loginID["state"] = "normal"
    else:
        # set not connected
        print("Status: Not connected")
        self.netStatus.configure(text='Internet: Not Connected', fg='red')
        # self.Sub_loginID["state"] = "disabled"

# fuction to check internet connectivity
def is_connected(self):
    try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

if 'app_update' in os.environ:
    root.update_idletasks()
else:
    root.mainloop()