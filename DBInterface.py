import pymysql
import sshtunnel
import hashlib

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

# Adds a new row to patient table in database
def addPatient(name, address, city, state, zip_code, phone_no = None, email = None, social = None, insurance = None):
    patient_id = genID(name + address)
    successfulInsert = False
    # While loop avoids conflicting patient_id hashes
    while(successfulInsert == False):
        # Generate mysql statement and send to database
        try: 
            sql = "INSERT INTO patient (patient_id, patient_name, address, city, state, zip) \
                VALUES('" + patient_id + "', '" + name + "', '" + address + "', '" + city + "', '" + state + "', " + str(zip_code) + ")"
            sendSQL(sql)
            successfulInsert = True
        # Generate new patient_id if conflict
        except pymysql.err.IntegrityError:
            patient_id = genID(patient_id)

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
        connection.commit()
        connection.close()

# basic 10-digit hashing function
def genID(hashString):
    newID = hashlib.sha1(hashString.encode("UTF-8")).hexdigest()
    newID = newID[:10]
    return(newID)
