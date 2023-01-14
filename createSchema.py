#Firestore DB: FlaskFire

from flask import jsonify
import uuid, cryptify, login
import datetime

def createSampleSchemaData(db):
	user_id = ''
	#User 
	try:
		user_data = {
			u'user_first_name': u'broleg',
			u'user_last_name': u'brolisalv',
            u'user_mobile': u'123131241244234',
            u'user_email': u'oleg@agent.com',
            u'user_address': u'Bloomington, IN',
			u'user_title': u'Agent',
			u'user_gender': u'N/A',
			u'user_age': u'50',
			u'user_height': u'150',
			u'user_weight': u'100',
			u'user_address': u'America',
			u'user_city': u'NYC',
			u'user_zipcode': u'1231232',
            u'role_id': u'3', #Patient 1, Doc 2, Agent 3
			u'plan_id': u'N/A'
        }
		user_id = generateUUID()
		db.collection(u'User').document(user_id).set(user_data)
		
		loginSchema(db, user_id)
		roleSchema(db)
		insuranceAgentSchema(db,user_id)
		#docSchema(db, user_id)
		#appointmentSchema(db)
		return jsonify({"success": True}), 200
	except Exception as e:
		return  f"An Error Occurred While Creating User Schema: {e}"

def loginSchema(db, user_id):
	hashedPw = cryptify.encrypt("ihatepeople")
	login_data = {
		u'login_username': u'brodius',
		u'login_password': hashedPw
	}
	if not login.userExists(db,"brodius"):
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

def appointmentSchema(db,user_id,patient_id):
	appointment_data = {
		u'doc_user_id': u'XXX',
		u'patient_user_id': u'YYY',
		u'time': datetime.utcnow(),
		u'note':"Meet me in the South cabin",
		u'type': "urgent" #(general, follow-up, urgent)
	}
	db.collection(u'Appointment').document(generateUUID()).set(appointment_data)

def insuranceAgentSchema(db,user_id):
    agent_data ={
        u'agency_name': u'IUInsurance',
        u'customer_range': u'bronze' #(bronze,gold,diamond)
    }
    db.collection(u'IAgent').document(user_id).set(agent_data)

def insurancePlanSchema(db,agent_id,patient_id):
	health_plan_data ={
		u'agent_user_id': u'XXX',
		u'plan_type': "bronze", #(bronze,gold,diamond)
		u'monthly_premium': u'$1000'
	}
	db.collection(u'IPlan').document(generateUUID()).set(health_plan_data)

def generateUUID():
	return str(uuid.uuid4())[:8]