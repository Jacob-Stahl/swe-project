# swe-project

  
<h1>Hospital Management System Manual</h1>

Dependencies:
python3
pip install:
<ul>
	<li>pymysql</li>
	<li>sshtunnel</li>
	<li>hashlib</li>
	<li>tkinter</li>
	<li>smtplib</li>
	<li>socket</li>
</ul>
Test logins
<ul>
	<li>Username            Password</li>
	<li>testDoctor          softeng3365</li>
	<li>testNurse           softeng3365</li>
	<li>testClerk           softeng3365</li>
	<li>testceo             softeng3365</li>
</ul>
Dummy Logins
<ul>
	<li>Patient ID:          f7e57ea675</li>
	<li>Appointment ID:     4d4dfb3fb2, 75fda9d96e</li>
</ul>

	
Run master.py to login. You will login as 1 of 4 kinds of staff

<ul>
	<li>Clerk<ul>
		<li> Add Appointment - set an appointment for a patient and enter their information</li>
		<li>  Edit Appointment - edit fields in existing appointment</li> 
		<li>  Delete Appointment - delete appointment</li> 
		<li>  View Appointment - look at existing appointment</li> 
		<li> Check-In Patient - search for a patient when they arrive and check them in</li> 
	</ul>
	<li>Doctor<ul>
		<li>  View Appointment - view a patients appointment information</li> 
		<li> View Patient Measurements - view patients measurements recorded by a nurse</li> 
		<li> Add Treatment - add a treatment and prescription</li> 
	</ul></li>
	<li>Nurse<ul>
		<li> Update Measurements - enter patient's measurements before they see the doctor</li> 
	</ul>
	<li>CEO<ul>
		<li> View Report - view weekly financial report</li> 
	</ul></li>
</ul>
