import pymysql
import sshtunnel
import hashlib

__name__ = 'DBInterface'

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

# NOTE: ALL 'date' entries MUST be formatted 'YYYY-MM-DD'

# Function to add treatment and prescription to a record
# can also overwrite treatment and prescription for a given record
# Returns True if successful, False if not
# For use by doctor after the nurse has already created a record
# Provide record_id, patient_id, or both
# If you provide neither, function will return False and won't do anything
# If you provide both, the function will ensure that the record's patient_id matches the patient_id provided
#   so providing both is slower than just providing one.
# If you provide only a patient_id and the patient has multiple records, the latest record will be used

def addTreatment(treatment, prescription, record_id = None, patient_id = None):
    # code to make sure correct record is found
    if record_id == None and patient_id == None:
        # return if neither patient_id nor record_id were provided
        return False
    # If only record_id was provided
    if patient_id == None:
        record = record_id
    # Get newest record og patient if only patient_id was provided
    elif record_id == None:
        patient = patient_id
        record = sendSQL("SELECT record_id FROM record WHERE patient_id = '" + patient + "' ORDER BY date DESC;")[0]
    # Make sure record_id and patient_id match if both record_id and patient_id were provided
    else:
        # try except blocks because I'm too lazy to debug edge cases
        # when ids are correct it should work fine
        try:
            record = record_id
            patient = patient_id
            recordsPatient = sendSQL("SELECT patient_id FROM record WHERE record_id = '" + record_id + "';")[0]
            if patient != recordsPatient:
                return False
        except:
            return False
    sendSQL("UPDATE record SET treatment = '" + treatment + "' WHERE record_id = '" + record + "';")
    sendSQL("UPDATE record SET prescription = '" + prescription + "' WHERE record_id = '" + record + "';")
    return True


# Basic function to create a record, intended for Nurse
def addRecord(patient_id, date, visit_reason, weight, height, blood_pressure):
    record_id = genID(patient_id + date)
    addRecordSQL = "INSERT INTO record (record_id, patient_id, date, visit_reason, weight, height, blood_pressure) \
        VALUES ('" + record_id + "', '" + patient_id + "', '" + date + "', '" + visit_reason + "', '" + weight + "', '" + height + "', '" + blood_pressure + "');"
    sendSQL(addRecordSQL)


# Create a new appointment entry in DB
# Includes preventative measures for duplicate entries
# Failure return codes:
#   "NAD" if docName provided references an employee that is not of classification "doctor"
#   "DNF" if not doctor of name docName was found in database
#   "AAE" if an appointment already exists for the specified date + time + doctor
def addAppointment(patient_name, patient_birthday, gender, docName, date, time, appointmentID = None):
    # Get doctor ID from docName
    docInfo = getEmployeeInfo(employee_name = docName)
    if docInfo != None:
        if docInfo[3].lower() == 'doctor':
            docID = docInfo[2]
        else:
            # Return code "NAD" if employee provided is not a doctor
            return "NAD"
    else:
        # Return code "DNF" if doctor was not found in database
        return "DNF"
    # Insert appointment
    successfulInsert = False
    if appointmentID == None:
        apt_id = genID(date + time + docID)
    else:
        apt_id = appointmentID
    # while loop avoids conflicting apt_id hashes
    while successfulInsert == False:
        try:
            getPatientSQL = "SELECT patient_id FROM patient WHERE patient_name = '" + patient_name + \
                "' AND birthday = '" + patient_birthday + "';"
            patient_id = sendSQL(getPatientSQL)
            # create new patient record if patient does not exist in database
            if patient_id == None:
                patient_id = addPatient(patient_name, patient_birthday, gender=gender)
            # set patient id if patient already exists in database
            elif len(patient_id) == 1:
                patient_id = patient_id[0]
            # throw exception if multiple patients w/ same name & birthday found
            else:
                raise LookupError('Multiple patients exist with provided name and birthday.')
            # Create SQL statement to add appointment to DB
            addAppSQL = "INSERT INTO appointment (apt_id, patient_id, patient_name, doctor_id, date, time) \
                VALUES ('" + apt_id + "', '" + patient_id + "', '" + patient_name + "', '" + docID + "', '" + date + "', '" + time + "');"
            sendSQL(addAppSQL)
            successfulInsert = True
        # catches duplicate entries and conflicting hashes
        except pymysql.err.IntegrityError:
            # differentiates duplicate entries from conflicting hashes
            if str(sendSQL("SELECT date FROM appointment WHERE apt_id = '" + apt_id + "';")[0]) != date:
                apt_id = genID(apt_id)
            else:
                # returns code "AAE" if appointment already exists for provided date and time
                return "AAE"
    # Returns appointment ID if appointment scheduling was successful
    return apt_id


# Adds payment information to appointment table.
# Returns True if successful
# Returns False if not
# 'amount' should be a float value, 'payment_type' is a string e.g. 'debit', 'credit', 'cash', etc
def addPayment(appointment_id, amount, paymentType, card_no = None, nameOnCard = None, exp = None):
    try:
        SQLPay = "UPDATE appointment SET paid = " + str(amount) + " WHERE apt_id = '" + appointment_id + "';"
        SQLPayment = "UPDATE appointment SET payment = '" + paymentType + "' WHERE apt_id = '" + appointment_id + "';"
        sendSQL(SQLPay)
        sendSQL(SQLPayment)
        if paymentType.lower() == 'credit' or paymentType.lower() == 'debit':
            SQLCardInfo = "UPDATE appointment SET card_no = '" + str(card_no) + "', card_name = '" + nameOnCard + "', exp = '" + str(exp) \
                + "' WHERE apt_id = '" + appointment_id + "';"
            sendSQL(SQLCardInfo)
        return True
    except:
        return False


# Adds a new row to patient table in database
# No preventative measures for duplicate entries
def addPatient(name, birthday, gender = None, address = None, city = None, state = None, zip_code = None, \
    phone_no = None, email = None, social = None, insurance = None):

    patient_id = genID(name + birthday)
    successfulInsert = False
    # While loop avoids conflicting patient_id hashes
    while(successfulInsert == False):
        # Generate mysql statement and send to database
        try: 
            sql1 = "INSERT INTO patient (patient_id, patient_name, birthday, gender"
            sql2 = "VALUES('" + patient_id + "', '" + name + "', '" + birthday + "', '" + gender
            if address != None:
                sql1 = sql1 + ", address, city, state, zip"
                sql2 = sql2 + "', '" + address + "', '" + city + "', '" + state + "', " + str(zip_code)
            sql1 = sql1 + ") "
            sql = sql1 + sql2 + "');"
            sendSQL(sql)
            successfulInsert = True
        # Generate new patient_id if conflict
        except pymysql.err.IntegrityError:
            patient_id = genID(patient_id)
    # Return patient id as confirmation
    return patient_id


# Function to add address, contact info, insurance, etc to patient by patient_id
# All values must be provided
# Returns True if successful, False if not
def addPatientInfo(patient_id, address, city, state, zip_code, phone_no, email, social, insurance):
    patient_name = sendSQL("SELECT patient_name FROM patient WHERE patient_id = '" + patient_id + "';")
    if patient_name != None:
        try:
            sendSQL("UPDATE patient SET address = '" + address + "', city = '" + city + "', state = '" + state + "', zip = " + str(zip_code) + \
                ", phone_no = '" + phone_no + "', email = '" + email + "', social = '" + social + "', insurance = '" + insurance + "' \
                    WHERE patient_id = '" + patient_id + "';")
            return True
        except:
            return False
    else:
        return False


# This function deletes an appointment from the database by appointment ID
# Returns True if successful
# Returns False if appointment was not found in database
def deleteAppointment(apt_id):
    appointment = getAppointment(appointment_id = apt_id)
    if appointment == "ANF":
        # appointment not found
        return False
    else:
        delSQL = "DELETE FROM appointment WHERE apt_id = '" + apt_id + "';"
        sendSQL(delSQL)
        return True


# This function will update any field in the appointment table
# First parameter is the appointment_id, and any combination of the subsequent parameters can be provided and all will be updated
# This function has to do a lot of weird stuff and interface with multiple tables, so it is slow
# Most input cases have been provided, but I could not test all of them, so let me know if you find an input combination that doesn't work
# return code "PNF" means patient provided was not found
# return code "DNF" means doctor provided was not found
def updateAppointment(appointment_id, patient_name = None, patient_birthday = None, gender = None, docName = None, date = None, time = None, ref_no = None):
    # get patient_id from patient_name
    if patient_name != None:
        patient_id = getPatientInfo(patient_name = patient_name, outField = 'patient_id')
        if patient_id != None:
            patient_id = patient_id[0]
        elif patient_birthday != None and gender != None:
            patient_id = addPatient(patient_name, patient_birthday, gender = gender)
        else:
            # Patient not found
            return "PNF"
    else:
        patient_id = None
    # get doctor ID from docName
    if docName != None:
        docID = sendSQL("SELECT employee_id FROM employee WHERE position = 'doctor' AND name = '" + docName + "';")
        if docID != None:
            docID = docID[0]
        else:
            # doctor not found
            return "DNF"
    else:
        docID = None
    # Create new apt info array
    newApt = [appointment_id, patient_id, patient_name, docID, date, time, None, None, None, None, None, ref_no]
    ogApt = getAppointment(appointment_id = appointment_id)
    updatedApt = []
    for i in range(len(newApt)):
        if str(newApt[i]) != str(ogApt[i]) and newApt[i] != None:
            updatedApt.append(newApt[i])
        else:
            updatedApt.append(ogApt[i])
    patientInfo = getPatientInfo(patient_id = updatedApt[1])
    doctor_name = sendSQL("SELECT name FROM employee WHERE employee_id = '" + updatedApt[3] + "';")[0]
    deleteAppointment(appointment_id)
    addAppointment(updatedApt[2], str(patientInfo[2]), patientInfo[3], doctor_name, str(updatedApt[4]), str(updatedApt[5]), appointmentID = updatedApt[0])
    if updatedApt[11] != None:
        refSQL = "UPDATE appointment SET ref_no = '" + str(updatedApt[11]) + "' WHERE apt_id = '" + appointment_id + "';"
        sendSQL(refSQL)


# General function that sends mysql statement to remote database through ssh tunnel
def sendSQL(sqlString, fetchAll = False):
    # login to ssh
    with sshtunnel.SSHTunnelForwarder(
        ('193.27.13.69', 4067),
        ssh_username='dbaccess', ssh_password='softeng3365',
        remote_bind_address=('127.0.0.1', 3306)
    ) as tunnel:
        # login to mysql
        connection = pymysql.connect(
            user='dbaccess', passwd='softeng3365',
            host='127.0.0.1', port=tunnel.local_bind_port,
            db='healthcare',
        )
        # send mysql statement & close connection
        with connection.cursor() as cursor:
            cursor.execute(sqlString)
            if fetchAll == False:
                result = cursor.fetchone()
            elif fetchAll == True:
                result = cursor.fetchall()
        connection.commit()
        connection.close()
    return result


# basic 10-digit hashing function
def genID(hashString):
    newID = hashlib.sha1(hashString.encode("UTF-8")).hexdigest()
    newID = newID[:10]
    return(newID)
    

# Simple patient SQL query function for use wherever needed
# Pass EITHER patient name OR patient id
#   If you pass BOTH the function will return nothing
#       because I'm too lazy to code a verification to make sure the name and id both match
# If you leave outField == None, function will return all info on patient stored in table
# Or, set outfield = field where field is a string that matches a parameter in the patient table
#   This will return the single value needed for the patient specified
def getPatientInfo(patient_name = None, patient_id = None, outField = None):
    if patient_name == None and patient_id == None:
        return
    elif patient_name != None and patient_id != None:
        return
    if outField == None:
        selectFieldTxt = "*"
    else:
        selectFieldTxt = outField
    if patient_name == None:
        whereFieldTxt1 = "patient_id"
        whereFieldTxt2 = patient_id
    else:
        whereFieldTxt1 = "patient_name"
        whereFieldTxt2 = patient_name
    SQLTxt = "SELECT " + selectFieldTxt + " FROM patient WHERE " + whereFieldTxt1 + " = '" + whereFieldTxt2 + "';"
    result = sendSQL(SQLTxt)
    return result


# get employee data from either employee_name or from employee's username
def getEmployeeInfo(employee_name = None, username = None):
    if username == None and employee_name != None:
        SQLSearch = "SELECT name, username, employee_id, position FROM employee WHERE name = '" + employee_name + "';"
        return sendSQL(SQLSearch)
    elif employee_name == None:
        SQLSearch = " SELECT name, username, employee_id, position FROM employee WHERE username = '" + username + "';"
        return sendSQL(SQLSearch)
    else: return None

# get record from either patient_id or record_id
# if patient_id only provided, will return patient's latest record
# if both patient_id and record_id are provided, function defaults to record_id and ignores patient_id
def getRecord(patient_id = None, record_id = None):
    if patient_id == None and record_id == None:
        return None
    elif record_id == None:
        SQLSearch = "SELECT * FROM record WHERE patient_id = '" + patient_id + "' ORDER BY date DESC;"
        record = sendSQL(SQLSearch, fetchAll = True)
        if record == None:
            # patient not found
            return "PNF"
        else:
            return record[0]
    else:
        SQLSearch = "SELECT * FROM record WHERE record_id = '" + record_id + "';"
        record = sendSQL(SQLSearch)
        if record == None:
            # record not found
            return "RNF"
        else:
            return record


# get appointment information from either patient_id or appointment_id
# if patient_id only provided, will return patient's latest appointment
# if both patient_id and appointment_id are provided, function defaults to using appointment_id and ignores patient_id
def getAppointment(patient_id = None, appointment_id = None):
    if patient_id == None and appointment_id == None:
        return None
    elif appointment_id == None:
        SQLSearch = "SELECT * FROM appointment WHERE patient_id = '" + patient_id + "' ORDER BY date DESC;"
        appointment = sendSQL(SQLSearch, fetchAll = True)
        if appointment == None:
            # patient not found
            return "PNF"
        else:
            return appointment[0]
    else:
        SQLSearch = "SELECT * FROM appointment WHERE apt_id = '" + appointment_id + "';"
        appointment = sendSQL(SQLSearch)
        if appointment == None:
            # appointment not found
            return "ANF"
        else:
            return appointment


# Function to getch billing report information from apt_id
# returns tuple [amount, payment_type, card_no, name_on_card, expiration_date, ref_no]
def getBilling(apt_id):
    billSQL = "SELECT paid, payment, card_no, card_name, exp, ref_no FROM appointment WHERE apt_id = '" + apt_id + "';"
    billingStatement = sendSQL(billSQL, fetchAll = True)
    if billingStatement != None:
        return billingStatement
    else:
        # appointment not found
        return "ANF"


# Lists all unique patient_ids
def listPatients():
    SQLSearch = "SELECT patient_id FROM patient;"
    return sendSQL(SQLSearch, fetchAll = True)

# Lists all doctors by name
# Lists by id if listIDs == True
def listDoctors(listIDs = False):
    if listIDs == False:
        SQLSearch = "SELECT name FROM employee WHERE position = 'doctor';"
    else:
        SQLSearch = "SELECT employee_id FROM employee WHERE position = 'doctor';"
    return sendSQL(SQLSearch, fetchAll = True)


# Input doctor name and date to get report on that doctor for that day
# returns a 4-value list:
#   [docName, docID, no_of_appointments, revenue_earned]
def createReport(docName, date):
    docID = sendSQL("SELECT employee_id FROM employee WHERE position = 'doctor' AND name = '" + docName + "';")
    if docID != None:
        docID = docID[0]
    else:
        # doctor not found
        return "DNF"
    aptList = sendSQL("SELECT apt_id FROM appointment WHERE doctor_id = '" + docID + "' AND date = '" + str(date) + "';", fetchAll = True)
    no_of_apt = len(aptList)
    paidList = []
    for apt in aptList:
        paidList.append(sendSQL("SELECT paid FROM appointment WHERE apt_id = '" + apt[0] + "';", fetchAll = True))
    totalEarned = 0
    for payment in paidList:
        if payment != None:
            totalEarned = totalEarned + payment[0][0]
    return [docName, docID, no_of_apt, float(totalEarned)]