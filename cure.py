import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
from createSchema import createSampleSchemaData
import filterDoc, cryptify, login, appointment, insurance
from flask_cors import CORS 


app = Flask(__name__)
CORS(app)

cred = credentials.Certificate('credentials/flaskfiremekey.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Doctor')

@app.route('/createSchema', methods=['GET', 'POST'])
def createSample():
	return createSampleSchemaData(db)

@app.route('/list', methods=['GET'])
def read():
    #     read() : Fetches "User" details and related fields if the user is also a "Doctor" or an insurance agent.
    #     todo_id : id passed in the URL
    try:
        ref_user = db.collection(u'User')
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            userDoc = ref_user.document(todo_id).get()
            return jsonify(filterDoc.unifyDoctorOrAgentFieldsToDict(db, userDoc)), 200
        else:
            outDocs = []
            for userDoc in ref_user.stream():
                outDocs.append({str(userDoc.id) : filterDoc.unifyDoctorOrAgentFieldsToDict(db, userDoc)})
            return jsonify(outDocs), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/add', methods=['GET', 'POST'])
def create():
    """
        Adds a document into "Doctor" collection. Provide ?id= as a field in URL. 
    """
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        Updates a document into "Doctor" or "IAgent" collection. Id required in POST. 
    """
    try:
        
        id = request.json.pop('id')
        userDoc = db.collection(u'User').document(id)
        userDict = userDoc.get().to_dict()
        role_id = userDict.pop("role_id")
        if role_id == "2":
            db.collection('Doctor').document(id).update(request.json)
        elif role_id == "3":
            db.collection('IAgent').document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/updateUser', methods=['POST', 'PUT'])
def updateUser():
    """
        Updates a document for any USER specific fields. Id required in POST. 
    """
    try:
        id = request.json.pop('id')
        print(request.json, type(request.json), "login_password" in request.json)
        if "login_password" in request.json:
            newpw = cryptify.encrypt(request.json.pop("login_password"))
            db.collection('Login').document(id).update({"login_password": newpw})
        db.collection(u'User').document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from "Doctor" collection. Provide ?id= as a field in URL.
    """
    try:
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    #TODO reset the cookies. Invalid current cookie. 
    return

@app.route('/login',methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        # {"userid": "idkas", "password": "hobbies", "request":"login" }
        if request.json['request'] == 'login':
            return login.login(db, request.json)        
        
        # {"request":"signUp", "user_first_name": "Neil", "user_last_name": "Armstrong", "user_mobile": "1232342488", "user_email": "neil@armstrong.com", "user_title": "Mr", "user_gender": "Male", "user_age": "92", "user_height": "182", "user_weight": "68", "user_address": "02, Crater Avenue", "user_city": "MoonCity", "user_zipcode": "3825968", "login_username": "neilbaba", "login_password": "neilbaba"}
        if request.json['request'] == 'signUp':
            return login.createUser(db, request.json)

        # {"login_username": "idkas", "request":"ifExists" }
        if request.json['request'] == 'ifExists':
            if login.userExists(db, request.json["login_username"]):
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False}), 200

@app.route('/filterDoc', methods=['GET', 'POST'])
def filter_doc():
    if request.method == 'POST':
        # {"user_first_name" || "user_last_name": "X", "request": "filterByname"}
        if request.json['request'] == 'filterByname':
            return filterDoc.filterDocByName(db, request)
        
        # {"request": "filterBysupports_covid"}
        if request.json['request'] == 'filterBysupports_covid':
            return filterDoc.filterDocBySupportsCovid(db, request)
        
        # {"speciality": "Cardiologist", "request": "filterByspeciality"}  
        if request.json['request'] == 'filterByspeciality':
            return filterDoc.filterBySpeciality(db, request)
                    
        # {"hospital_name": "IUHospital", "request": "filterByhospital_name"} 
        if request.json['request'] == 'filterByhospital_name':
            return filterDoc.filterByHospital(db, request)

@app.route('/appointment', methods=['GET', 'POST'])
def appoint():
    if request.method == 'POST':
        # {"request": "schedule_appointment", "appointment_id": "V", "patient_user_id": "X", "note": "ABC", "type": "general/follow-up/urgent"}
        if request.json['request'] == 'schedule_appointment':
            return appointment.scheduleAppointment(db, request)

        # {"request": "upcoming_patient_appointments", "patient_user_id": "X"}
        if request.json['request'] == 'upcoming_patient_appointments':
            return appointment.upcomingUserApts(db, request)

        # {"request": "view_patient_appointments", "doc_user_id": "X"}
        if request.json['request'] == 'view_patient_appointments':
            return appointment.viewPatientApts(db, request)

        # Exclusive to doc ->#
        # {"request": "add_doctor_slot", "doc_user_id": "X", "time": "2022-11-13T11:16:41", "note": "Meet me in South Cabin"}
        if request.json['request'] == 'add_doctor_slot':
            return appointment.addDoctorSlot(db, request)

        # {"request": "view_doctor_appointments", "doc_user_id": "X"}
        if request.json['request'] == 'view_doctor_appointments':
            return appointment.viewDocApts(db, request, 0)

        # {"request": "upcoming_doctor_appointments", "doc_user_id": "X"}
        if request.json['request'] == 'upcoming_doctor_appointments':
            return appointment.viewDocApts(db, request, 3)

        # {"request": "view_doctor_slots", "doc_user_id": "X"}
        if request.json['request'] == 'view_doctor_slots':
            return appointment.viewDocApts(db, request, 1)

        # {"request": "update_supports_covid_beds", "doc_user_id": "X", "supports_covid": 22}
        if request.json['request'] == 'update_supports_covid_beds':
            return appointment.update_supports_covid_beds(db, request)
                

@app.route('/insurance', methods=['GET', 'POST'])
def insure():
    if request.method == 'POST':
        # {"request": "set_plan", "plan_id": "V","patient_user_id": "X"}
        if request.json['request'] == 'set_plan':
            return insurance.setIPlan(db, request)

        # {"request": "add_IPlan","agent_user_id": "X", "plan_type": "bronze/gold/diamond, "monthly_premium":"$3"
        if request.json['request'] == 'add_IPlan':
            return insurance.addIPlan(db,request)

        # {"request": "update_IPlan", "plan_id": "V", "plan_type": "bronze/gold/diamond, "monthly_premium":"$8"
        if request.json['request'] == 'update_IPlan':
            return insurance.updateIPlan(db,request)

        # {"request": "view_agent_plans", "agent_user_id": "X"}
        if request.json['request'] == 'view_agent_plans':
            return insurance.viewAgentPlans(db, request)

        # {"request": "get_total_and_recurring_bills", "patient_user_id": "X"}
        if request.json['request'] == 'get_total_and_recurring_bills':
            return insurance.get_total_and_recurring_bills(db, request)


@app.route('/',methods=['GET', 'POST'])
def ssd():
    return render_template("index.html")

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)