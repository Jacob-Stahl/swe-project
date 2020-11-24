import pymysql
import sshtunnel
import hashlib

__name__ = 'DBInterface'

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


# Create a new appointment entry in DB
# Not finished!!
def addAppointment(patient_name, patient_birthday, gender, date, time):
    apt_id = genID(date + time)
    getPatientSQL = "SELECT patient_id FROM patient WHERE patient_name = '" + patient_name + \
        "AND birthday = " + patient_birthday + "';"
    patient_id = sendSQL(getPatientSQL)
    # set patient id if patient already exists in database
    if len(patient_id == 1):
        patient_id = patient_id[0]
    # create new patient record if patient does not exist in database
    elif len(patient_id == 0):
        patient_id = addPatient(patient_name, patient_birthday, gender=gender)
    # throw exception if multiple patients w/ same name & birthday found
    else:
        raise LookupError('Multiple Patients exist with provided name and birthday')
    

# Adds a new row to patient table in database
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
    # Return patiend id as confirmation
    return patient_id


# General function that sends mysql statement to remote database through ssh tunnel
def sendSQL(sqlString, createID = False):
    # login to ssh
    with sshtunnel.SSHTunnelForwarder(
        ('193.27.13.94', 4067),
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
            result = cursor.fetchone()
        connection.commit()
        connection.close()
    return result


# basic 10-digit hashing function
def genID(hashString):
    newID = hashlib.sha1(hashString.encode("UTF-8")).hexdigest()
    newID = newID[:10]
    return(newID)
    