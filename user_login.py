import DBInterface
import hashlib

__name__ = 'user_login'


# Function to login using hashed passwords in employee table on DB
def login(username, password):
    # Fetch info on employee attempting to login
    emp_info = DBInterface.sendSQL("SELECT * FROM employee WHERE username = '" + username + "';")
    # If employee was found in DB
    if emp_info != None:
        # Hash provided password
        passHash = hashlib.sha256(password.encode("UTF-8")).hexdigest()
        storedHash = emp_info[1]
        # Check if hash matches DB
        if passHash == storedHash:
            # Return logged in user object if successful
            currentUser =  user(emp_info[0], emp_info[2], emp_info[3], emp_info[4])
            return currentUser
        # Incorrect Password
        else:
            return "PW"
    # User not found
    else:
        return "USR"


# User object providing basic info on user currently logged in
# Can be used to determine what interfaces to bring up
# As well as permissions depending on employee position (classification)
class user:
    def __init__(self, employee_id, username, name, classification):
        self.name = name
        self.employee_id = employee_id
        self.classification = classification