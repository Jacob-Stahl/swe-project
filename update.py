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

class App:
    def __init__(self, master):

        self.master = master
        # heading label
        self.heading = Label(master, text="Update Appointments",  fg='black', font=('arial 18'))
        self.heading.place(x=180, y=40)

        # search criteria -->name 
        self.name = Label(master, text="Enter Appointments ID", font=('arial 12'))
        self.name.place(x=70, y=100)

        # entry for  the name
        self.namenet = Entry(master, width=30)
        self.namenet.place(x=300, y=100)

        # search button
        self.search = Button(master, text="Search", width=12, height=1, bg='steelblue', command=self.search_db)
        self.search.place(x=230, y=150)
    
    # function to search
    def search_db(self):
        self.input = self.namenet.get()

        self.res = getAppointment(self.input)

        self.patient_name = self.res[0]
        self.patient_birthday = self.res[1]
        self.gender = self.res[2]
        self.docName = self.res[3]
        self.date = str(self.res[4])
        self.time = str(self.res[5])
        
        # creating the update form
        self.uname = Label(self.master, text="Patient's Name", font=('arial 12'))
        self.uname.place(x=70, y=220)

        self.uage = Label(self.master, text="Age", font=('arial 12'))
        self.uage.place(x=70, y=260)

        self.ugender = Label(self.master, text="Gender", font=('arial 12'))
        self.ugender.place(x=70, y=300)

        self.ulocation = Label(self.master, text="Doctor Name", font=('arial 12'))
        self.ulocation.place(x=70, y=340)

        self.utime = Label(self.master, text="Appointment Date (YYYY-MM-DD)", font=('arial 12'))
        self.utime.place(x=70, y=380)

        self.uphone = Label(self.master, text="Appointment Time (HH:MM)", font=('arial 12'))
        self.uphone.place(x=70, y=420)

        # entries for each labels ============================================= filling the search result in the entry box to update
        self.ent1 = Entry(self.master, width=30)
        self.ent1.place(x=300, y=220)
        self.ent1.insert(END, str(self.patient_name))

        self.ent2 = Entry(self.master, width=30)
        self.ent2.place(x=300, y=260)
        self.ent2.insert(END, str(self.patient_birthday))

        # gender list
        GenderList = ["Male", "Female", "Transgender"]

        # Option menu
        self.var = tk.StringVar()
        self.var.set(GenderList[0])

        self.opt = tk.OptionMenu(self.master, self.var, *GenderList)
        self.opt.config(width=10, font=('arial', 11))
        self.opt.place(x=300, y=300)

        # callback method
        def callback(*args):
            for i in range(len(GenderList)):
                if GenderList[i] == self.var.get():
                    # print(GenderList[i])
                    self.gender = GenderList[i]
                    break

        self.var.trace("w", callback)

        self.ent4 = Entry(self.master, width=30)
        self.ent4.place(x=300, y=340)
        self.ent4.insert(END, str(self.docName))

        self.ent5 = Entry(self.master, width=30)
        self.ent5.place(x=300, y=380)
        self.ent5.insert(END, str(self.date))

        self.ent6 = Entry(self.master, width=30)
        self.ent6.place(x=300, y=420)
        self.ent6.insert(END, str(self.time))

        # button to execute update
        self.update = Button(self.master, text="Update", width=20, height=2, bg='lightblue', command=self.update_db)
        self.update.place(x=200, y=480)
    
    def update_db(self):
        # declaring the variables to update
        self.var1 = self.ent1.get()     #updated name
        self.var2 = self.ent2.get()     #updated age
        self.var3 = self.gender         #updated gender
        self.var4 = self.ent4.get()     #updated doctorName
        self.var5 = self.ent5.get()     #updated date
        self.var6 = self.ent6.get()     #updated time

        updateApp = updateAppointment(self.input, self.var1, self.var2, self.var3, self.var4, self.var5, self.var6, ref_no = None)

        if updateApp == "PNF":
            tkinter.messagebox.showerror("Failed", "Patient provided was not found")
        elif updateApp == "DNF":
            tkinter.messagebox.showerror("Failed", "Doctor provided was not found")
        else:
            tkinter.messagebox.showinfo("Updated", "Successfully Updated.")

#creating the object
root = tk.Tk()
b = App(root)
root.geometry("640x620+100+50")
root.resizable(False, False)
root.title("Update Appointment")
root.iconphoto(False, tk.PhotoImage(file='resources/icon.png'))

# end the loop
root.mainloop()