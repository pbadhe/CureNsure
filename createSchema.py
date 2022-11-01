#Firestore DB: FlaskFire

from flask import Flask, request, jsonify
import uuid
import crypt

def createSampleSchemaData(db):
	user_id = ''
	#User 
	try:
		user_data = {
			u'first_name': u'Oleg',
			u'last_name': u'Lyashchuk',
            u'user_name': u'idkas',
            u'user_mobile': u'123134234',
            u'user_email': u'oleg@iu.edu',
            u'user_address': u'Bloomington, IN',
            u'role_id': u'1', #Patient 1, Doc 2, Agent 3
            u'login_username': u'idkasOleg'
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
		#TODO check login_username duplication
		u'login_username': u'idkas',
		u'login_password': hashedPw
	}
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

# def delete_collection(coll_ref, batch_size):
#     docs = coll_ref.limit(batch_size).stream()
#     deleted = 0

#     for doc in docs:
#         print(f'Deleting doc {doc.id} => {doc.to_dict()}')
#         doc.reference.delete()
#         deleted = deleted + 1

#     if deleted >= batch_size:
#         return delete_collection(coll_ref, batch_size)