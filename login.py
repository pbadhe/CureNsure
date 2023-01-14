from flask import jsonify
import cryptify, uuid

def login(db, requestDict):
    login_input_username = requestDict['userid']
    login_input_password = requestDict['password']
    try:
        for doc in db.collection('Login').stream():
            if login_input_username == doc.to_dict()['login_username']:
                dbHashedPw = doc.to_dict()['login_password']
                if cryptify.checkPassword(login_input_password, dbHashedPw):
                    return jsonify({"Login_Success": True, "id":str(doc.id)}), 200
                else:
                    return jsonify({"Login_Success": "Invalid Password"}), 401

        return jsonify({"Login_Success": "Invalid Username"}), 401
    except Exception as e:
        return jsonify(f'Internal application error',e), 401

def createUser(db, requestDict):
    requestDict.pop("request")
    login_username = requestDict.pop("login_username")

    if not userExists(db, login_username):
        hashedPw = cryptify.encrypt(requestDict.pop("login_password"))
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
