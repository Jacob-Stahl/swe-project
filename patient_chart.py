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

# Connect to the databse.
conn = sqlite3.connect('database.db')

# Cursor to move in the database
c = conn.cursor()

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
        self.treatment_record = Label(self.left, text="Treatment Record", font=('arial 12'), fg='black', bg='lightblue')
        self.treatment_record.place(x=65, y=100)

        self.name = Label(self.left, text="Patient's Name", font=('arial 12'), fg='black', bg='lightblue')
        self.name.place(x=65, y=140)

        self.doctor_name = Label(self.left, text="Doctor Name", font=('arial 12'), fg='black', bg='lightblue')
        self.doctor_name.place(x=65, y=180)

        # Enteries for all labels
        self.treatment_record_ent = Entry(self.left, width=30)
        self.treatment_record_ent.place(x=275, y=100)

        self.name_ent = Entry(self.left, width=30)
        self.name_ent.place(x=275, y=140)
        
        self.doctor_name_ent = Entry(self.left, width=30)
        self.doctor_name_ent.place(x=275, y=180)

        self.db_designation = 'Nurse'

        if self.db_designation == 'Doctor':
            # Treatment
            self.treatment = Label(self.left, text="Treatment", font=('arial 12'), fg='black', bg='lightblue')
            self.treatment.place(x=65, y=220)

            self.treatment_ent = Entry(self.left, width=30)
            self.treatment_ent.place(x=275, y=220)

            # Prescription
            self.prescription = Label(self.left, text="Prescription", font=('arial 12'), fg='black', bg='lightblue')
            self.prescription.place(x=65, y=260)
            
            self.prescription_ent = Entry(self.left, width=30)
            self.prescription_ent.place(x=275, y=260)

        elif self.db_designation == 'Nurse':
            # Weight
            self.weight = Label(self.left, text="Weight", font=('arial 12'), fg='black', bg='lightblue')
            self.weight.place(x=65, y=220)
            
            self.weight_ent = Entry(self.left, width=30)
            self.weight_ent.place(x=275, y=220)

            # Height
            self.height = Label(self.left, text="Height", font=('arial 12'), fg='black', bg='lightblue')
            self.height.place(x=65, y=260)

            self.height_ent = Entry(self.left, width=30)
            self.height_ent.place(x=275, y=260)

            # Blood Pressure
            self.blood_pressure = Label(self.left, text="Blood Pressure", font=('arial 12'), fg='black', bg='lightblue')
            self.blood_pressure.place(x=65, y=300)

            self.blood_pressure_ent = Entry(self.left, width=30)
            self.blood_pressure_ent.place(x=275, y=300)

            # Reason for visit
            self.reason_for_visit = Label(self.left, text="Reason for visit", font=('arial 12'), fg='black', bg='lightblue')
            self.reason_for_visit.place(x=65, y=340)

            self.reason_for_visit_ent = Entry(self.left, width=30)
            self.reason_for_visit_ent.place(x=275, y=340)

        # button to perform a command
        self.submit = Button(self.left, text="Add Patient Chart", width=20, height=2, bg='steelblue', command=self.add_patient_chart)
        self.submit.place(x=190, y=400)

    # Gets triggered when the submit button is clicked
    def add_patient_chart(self, event):
        # getting the user inputs
        self.val1 = self.treatment_record.get()
        self.val2 = self.name_ent.get()
        self.val3 = self.doctor_name_ent.get()

        self.val4 = self.treatment_ent.get()
        self.val5 = self.prescription_ent.get()

        self.val6 = self.weight_ent.get()
        self.val7 = self.height_ent.get()
        self.val8 = self.blood_pressure_ent.get()
        self.val9 = self.reason_for_visit_ent.get()

        # Checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '' or self.val6 == '' or self.val7 == '' or self.val8 == '' or self.val9 == '':
            tkinter.messagebox.showwarning("Warning","Please fill up all the details")
        
        elif self.db_designation == 'Doctor':
            # Now we add to the database
            sql = "INSERT INTO 'appointments' (Treatment Record, Patient Name, Doctor Name, Treatment, Prescription) VALUES(?, ?, ?, ?, ?)"
            c.execute(sql, (self.val1, self.val2, self.val3, self.val4, self.val5))
            conn.commit()
            tkinter.messagebox.showinfo("Success","Appointment for "+ str(self.val1)+" has been created")

            self.box.insert(END, '\nAppointment fixed for ' + str(self.val1) + ' at ' + str(self.val3))        
        else:
            # Now we add to the database
            sql = "INSERT INTO 'appointments' (name, age, gender, location, assigned_doctor, scheduled_time, phone) VALUES(?, ?, ?, ?, ?, ?)"
            c.execute(sql, (self.val1, self.val2, self.val3, self.val6, self.val5, self.val6, self.val7))
            conn.commit()
            tkinter.messagebox.showinfo("Success","Appointment for "+ str(self.val1)+" has been created")

            self.box.insert(END, '\nAppointment fixed for ' + str(self.val1) + ' at ' + str(self.val5))

# Creating the object
root = tk.Tk()
b = App(root)

# Resolution of the window
root.geometry("580x500")

# Preventing the resize feature
root.resizable(False, False)

# Title of the window
root.title("Patient Chart")

# Icon of the application
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

root.bind('<Return>', b.add_patient_chart)

# End the loop
root.mainloop()