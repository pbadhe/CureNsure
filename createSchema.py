#Firestore DB: FlaskFire

from flask import jsonify
import uuid, crypt, login

def createSampleSchemaData(db):
	user_id = ''
	#User 
	try:
		user_data = {
			u'user_first_name': u'Oleg',
			u'user_last_name': u'Lyashchuk',
            u'user_mobile': u'123134234',
            u'user_email': u'oleg@iu.edu',
            u'user_address': u'Bloomington, IN',
			u'user_title': u'Mr',
			u'user_gender': u'Male',
			u'user_age': u'34',
			u'user_height': u'182',
			u'user_weight': u'68',
			u'user_address': u'Ukraine',
			u'user_city': u'Kyiv',
			u'user_zipcode': u'1231232',
            u'role_id': u'1' #Patient 1, Doc 2, Agent 3
        }
		user_id = str(uuid.uuid4())[:8]
		db.collection(u'User').document(user_id).set(user_data)
		
		loginSchema(db, user_id)
		roleSchema(db)
		docSchema(db, user_id)
		return jsonify({"success": True}), 200
	except Exception as e:
		return  f"An Error Occurred While Creating User Schema: {e}"

def loginSchema(db, user_id):
	hashedPw = crypt.encrypt("hobbies")
	login_data = {
		u'login_username': u'idkas',
		u'login_password': hashedPw
	}
	if not login.userExists("idkas"):
		db.collection(u'Login').document(user_id).set(login_data)

def roleSchema(db):
	role_data = {
		u'1': u'Patient',
		u'2': u'Doctor',
		u'3': u'IAgent',
	}
	db.collection(u'Role').document('RoleDoc').set(role_data)

def docSchema(db, user_id):
	login_data = {
		u'speciality': u'Cardiologist',
		#HospitalID or just Hospital Name? 
		u'hospital_name': u'IUHospital',
		u'supports_covid': u'1' #0 no, 1 yes
	}
	db.collection(u'Doctor').document(user_id).set(login_data)
