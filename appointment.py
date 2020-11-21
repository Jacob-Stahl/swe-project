# Adding support for python 2 & 3

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter as tk
    
import sqlite3
import tkinter.messagebox

# connect to the databse.
conn = sqlite3.connect('database.db')
# cursor to move in the database
c = conn.cursor()

# empty list to later appends the ids from the database
ids = []

# tkinter window
class App:
    def __init__(self, master):
        self.master = master

        # creating the format in master
        self.left = Frame(master, width=600, height=720, bg='lightblue')
        self.left.pack(side = LEFT)

        self.right = Frame(master, width=400, height=720, bg='steelblue')
        self.right.pack(side = RIGHT)

        # heading
        self.heading = Label(self.left, text="Enter details", font=('arial 18'), fg='black', bg='lightblue')
        self.heading.place(x=220, y=50)

        # patient's name
        self.name = Label(self.left, text="Patient's Name", font=('arial 12'), fg='black', bg='lightblue')
        self.name.place(x=65, y=100)

        # age
        self.age = Label(self.left, text="Age", font=('arial 12'), fg='black', bg='lightblue')
        self.age.place(x=65, y=140)

        # gender
        self.gender = Label(self.left, text="Gender", font=('arial 12'), fg='black', bg='lightblue')
        self.gender.place(x=65, y=180)

        # location
        self.location = Label(self.left, text="Location", font=('arial 12'), fg='black', bg='lightblue')
        self.location.place(x=65, y=220)

        # Doctor's name
        self.docName = Label(self.left, text="Doctor's Name", font=('arial 12'), fg='black', bg='lightblue')
        self.docName.place(x=65, y=260)

        # appointment time
        self.time = Label(self.left, text="Appointment Time (HH:MM)", font=('arial 12'), fg='black', bg='lightblue')
        self.time.place(x=65, y=300)

        # phone
        self.phone = Label(self.left, text="Phone Number", font=('arial 12'), fg='black', bg='lightblue')
        self.phone.place(x=65, y=340)

        # Enteries for all labels==============================================================
        self.name_ent = Entry(self.left, width=30)
        self.name_ent.place(x=275, y=100)

        self.age_ent = Entry(self.left, width=30)
        self.age_ent.place(x=275, y=140)

        # gender list
        GenderList = ["Male", "Female", "Transgender"]

        # Option menu
        self.var = tk.StringVar()
        self.var.set(GenderList[0])

        self.opt = tk.OptionMenu(self.master, self.var, *GenderList)
        self.opt.config(width=10, font=('arial', 11))
        self.opt.place(x=275, y=180)

        # callback method
        def callback(*args):
            for i in range(len(GenderList)):
                if GenderList[i] == self.var.get():
                    self.gender_ent = GenderList[i]
                    break
        
        self.var.trace("w", callback)

        self.location_ent = Entry(self.left, width=30)
        self.location_ent.place(x=275, y=220)


        self.doc_name_ent = Entry(self.left, width=30)
        self.doc_name_ent.place(x=275, y=260)

        self.time_ent = Entry(self.left, width=30)
        self.time_ent.place(x=275, y=300)

        self.phone_ent = Entry(self.left, width=30)
        self.phone_ent.place(x=275, y=340)

        # button to perform a command
        self.submit = Button(self.left, text="Add Appointment", width=20, height=2, bg='steelblue', command=self.add_appointment)
        self.submit.place(x=190, y=400)

    # function to call when the submit button is clicked
    def add_appointment(self, event):
        # getting the user inputs
        self.val1 = self.name_ent.get()
        self.val2 = self.age_ent.get()
        self.val3 = self.gender_ent
        self.val4 = self.location_ent.get()
        self.val5 = self.time_ent.get()
        self.val6 = self.phone_ent.get()
        self.val7 = self.doc_name_ent.get()

        # checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '' or self.val6 == '' or self.val7 == '':
            tkinter.messagebox.showwarning("Warning","Please fill up all the details")
        else:
            # now we add to the database
            sql = "INSERT INTO 'appointments' (name, age, gender, location, assigned_doctor, scheduled_time, phone) VALUES(?, ?, ?, ?, ?, ?)"
            c.execute(sql, (self.val1, self.val2, self.val3, self.val4, self.val5, self.val6, self.val7))
            conn.commit()
            tkinter.messagebox.showinfo("Success","Appointment for "+str(self.val1)+" has been created")
            
            self.box.insert(END, '\nAppointment fixed for ' + str(self.val1) + ' at ' + str(self.val5))


#creating the object
root = tk.Tk()
b = App(root)

# resolution of the window
root.geometry("600x520")

# preventing the resize feature
root.resizable(False, False)

# title of the window
root.title("Add new appointment")

# icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.add_appointment)

# end the loop
root.mainloop()