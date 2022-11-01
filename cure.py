import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
from createSchema import createSampleSchemaData
import logging
import crypt
import filterDoc

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
    """
        read() : Fetches "Doctor" data & related details from "User"
        todo_id : id passed in the URL
    """
    try:
        ref_doc = db.collection(u'Doctor')
        ref_user = db.collection(u'User')
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            todo = ref_doc.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            outDocs = []
            for doc in ref_doc.stream():
                k = ref_user.document(doc.id)
                logging.debug(f'{k.id} => {k.get().to_dict()}')
                outDocs.append(f'{k.id} => {k.get().to_dict()}')
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
def login():
    if request.method == 'POST':
        # {"userid": "idkas", "password": "hobbies", "request":"login" }
        if request.json['request'] == 'login':
            login_input_username = request.json['userid']
            login_input_password = request.json['password']
            try:
                for doc in db.collection('Login').stream():
                    if login_input_username == doc.to_dict()['login_username']:
                        dbHashedPw = doc.to_dict()['login_password']
                        if crypt.checkPassword(login_input_password, dbHashedPw):
                            logging.debug(f'Login successful for {login_input_username} user')
                            return jsonify({"Login Success": "True"}), 200
                        else:
                            return jsonify({"Login Success": "Invalid Password"}), 401

                return jsonify({"Login Success": "Invalid Username"}), 401
            except Exception:
                logging.debug(f'Login failed for {login_input_username}', Exception)
                return jsonify(f'Internal application error',Exception), 401

@app.route('/filterDoc', methods=['GET', 'POST'])
def filter_doc():
    if request.method == 'POST':
        # {"first_name" || "last_name": "LastNameInUserCollection", "request": "filterByname"}
        if request.json['request'] == 'filterByname':
            return filterDoc.filterDocByName(db,request)
        
        # {"request": "filterBysupports_covid"}
        if request.json['request'] == 'filterBysupports_covid':
            return filterDoc.filterDocBySupportsCovid(db,request)
        
        # {"speciality": "DoctorDefined", "request": "filterByspeciality"}  
        if request.json['request'] == 'filterByspeciality':
            return filterDoc.filterBySpeciality(db,request)
                    
        # {"hospital_name": "DoctorDefined", "request": "filterByhospital_name"} 
        if request.json['request'] == 'filterByhospital_name':
            return filterDoc.filterByHospital(db,request)


@app.route('/',methods=['GET', 'POST'])
def ssd():
    return render_template("index.html")

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)


