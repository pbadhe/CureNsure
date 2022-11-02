import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
from createSchema import createSampleSchemaData
import logging, filterDoc, login

app = Flask(__name__)

cred = credentials.Certificate('credentials/flaskfiremekey.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Doctor')

@app.route('/createSchema', methods=['GET', 'POST'])
def createSample():
	return createSampleSchemaData(db)

@app.route('/list', methods=['GET'])
def read():
    #     read() : Fetches "User" details and related fields if the user is also a "Doctor".
    #     todo_id : id passed in the URL
    try:
        ref_doc = db.collection(u'Doctor')
        ref_user = db.collection(u'User')
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            userDoc = ref_user.document(todo_id).get()
            return jsonify(filterDoc.unifyDoctorFieldsToDict(db, userDoc)), 200
        else:
            outDocs = []
            for userDoc in ref_user.stream():
                outDocs.append(f'{userDoc.id} => {filterDoc.unifyDoctorFieldsToDict(db, userDoc)}')
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
        Updates a document into "Doctor" collection. Id required in POST. 
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
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
            return filterDoc.filterDocByName(db,request)
        
        # {"request": "filterBysupports_covid"}
        if request.json['request'] == 'filterBysupports_covid':
            return filterDoc.filterDocBySupportsCovid(db,request)
        
        # {"speciality": "Cardiologist", "request": "filterByspeciality"}  
        if request.json['request'] == 'filterByspeciality':
            return filterDoc.filterBySpeciality(db,request)
                    
        # {"hospital_name": "IUHospital", "request": "filterByhospital_name"} 
        if request.json['request'] == 'filterByhospital_name':
            return filterDoc.filterByHospital(db,request)


@app.route('/',methods=['GET', 'POST'])
def ssd():
    return render_template("index.html")

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)


