import DBInterface
import hashlib

__name__ = 'user_login'

# -------HOW TO USE--------
# import this module w/ "import user_login"
# set currentUser = login(username, password)
# login queries are a lil slow thanks to those uber secure 256-bit hashes
# Failed logins will set currentUser to an error code:
#   currentUser == "PW" means incorrect password was entered
#   currentUser == "USR" means username was not found
# currentUser has 3 attributes:
#   currentUser.name: employee name
#   currentUser.employee_id: employee id as stored in DB
#   currentUser.classification: employee position, either 'doctor', 'nurse', or 'clerk'
# User currentUser.classification to determine what menus to pull up on login

# Test logins:
#   username        password
#   'testDoctor'     'softeng3365'
#   'testNurse'      'softeng3365'
#   'testClerk'      'softeng3365'
#   'testceo'        'softeng3365'
# Patient ID: 28edf3edc5, f7e57ea675


# Function to login using hashed passwords in employee table on DB
def loginUser(username, password):
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