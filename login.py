from flask import jsonify
import logging, crypt, uuid

def login(db, requestDict):
    login_input_username = requestDict['userid']
    login_input_password = requestDict['password']
    try:
        for doc in db.collection('Login').stream():
            if login_input_username == doc.to_dict()['login_username']:
                dbHashedPw = doc.to_dict()['login_password']
                if crypt.checkPassword(login_input_password, dbHashedPw):
                    logging.debug(f'Login successful for {login_input_username} user')
                    return jsonify({"Login Success": True, "id":str(doc.id)}), 200
                else:
                    return jsonify({"Login Success": "Invalid Password"}), 401

        return jsonify({"Login Success": "Invalid Username"}), 401
    except Exception as e:
        logging.debug(f'Login failed for {login_input_username}', e)
        return jsonify(f'Internal application error',e), 401

def createUser(db, requestDict):
    requestDict.pop("request")
    requestDict["role_id"] = "1"
    login_username = requestDict.pop("login_username")

    if not userExists(db, login_username):
        hashedPw = crypt.encrypt(requestDict.pop("login_password"))
        try:
            user_id = str(uuid.uuid4())[:8]
            db.collection(u'User').document(user_id).set(requestDict)
            db.collection(u'Login').document(user_id).set(
                {"login_username": login_username, "login_password": hashedPw})
            return jsonify({"success": True, "id":str(user_id)}), 200
        except Exception as e:
            return  f"An Error Occurred While Creating User : {e}"
    else:
        return jsonify({"success": False, "id":"Already Exists"}), 401

def userExists(db, login_username):
    for doc in db.collection('Login').stream():
        if login_username == doc.to_dict()['login_username']:
            return True
