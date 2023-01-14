from tokenize import Special
from flask import jsonify

def mergeDocsToDict(doc1, doc2):
    return dict(list(doc1.to_dict().items()) + list(doc2.to_dict().items()))

def unifyDoctorOrAgentFieldsToDict(db, userDoc):
    if db.collection('Doctor').document(userDoc.id).get().to_dict():
        return mergeDocsToDict(db.collection('Doctor').document(userDoc.id).get(), userDoc)
    elif db.collection('IAgent').document(userDoc.id).get().to_dict():
        return mergeDocsToDict(db.collection('IAgent').document(userDoc.id).get(), userDoc)
    else:
        return userDoc.to_dict()


def filterDocByName(db, request):
    first_name = request.json.get('user_first_name', ' ') #space; bcz comparing with '' below if no value exists 
    last_name = request.json.get('user_last_name', ' ')
    
    try:
        dbDoc = db.collection('Doctor')
        dbUser = db.collection('User')
        docFiltered = []
        for doc in dbDoc.stream():
            user = dbUser.document(doc.id).get()
            if user:
                first = user.to_dict().get('user_first_name','')
                last =  user.to_dict().get('user_last_name','')
                if first == first_name or last == last_name:
                    docFiltered.append({str(doc.id):mergeDocsToDict(doc,user)})
                
        if len(docFiltered) > 0:
            return jsonify(docFiltered), 200
        else:
            return f"No Doctors Found with names {first_name}, {last_name}", 200
    except Exception:
        return jsonify(f'Exception occured at filterByName',Exception), 401

def filterDocBySupportsCovid(db, request):
    try:
        dbDoc = db.collection(u'Doctor')
        dbUser = db.collection(u'User')
        filteredDoctors = []
        for curr in dbDoc.stream():
            if '' != curr.to_dict().get('supports_covid',''):
                userDoc = dbUser.document(curr.id).get()
                filteredDoctors.append({str(curr.id):mergeDocsToDict(userDoc, curr)})

        if len(filteredDoctors) > 0:
            return jsonify(filteredDoctors), 200
        else:
            return f"No Doctors Found who support covid treatment", 200

    except Exception:
        return jsonify(f'Exception occured at filterBySpeciality',Exception), 401
    return
 
def filterBySpeciality(db, request):
    speciality=request.json['speciality']
    try:
        dbDoc = db.collection(u'Doctor')
        dbUser = db.collection(u'User')
        filteredDoctors = []
        for curr in dbDoc.stream():
            if speciality == curr.to_dict()['speciality']:
                userDoc = dbUser.document(curr.id).get()
                filteredDoctors.append({str(curr.id):mergeDocsToDict(userDoc, curr)})

        if len(filteredDoctors) > 0:
            return jsonify(filteredDoctors), 200
        else:
            return f"No Doctors Found as {speciality}", 200

    except Exception:
        return jsonify(f'Exception occured at filterBySpeciality',Exception), 401

def filterByHospital(db,request):
    hospital=request.json['hospital_name']
    try:
        dbDoc = db.collection(u'Doctor')
        dbUser = db.collection(u'User')
        filteredDoctors = []
        for curr in dbDoc.stream():
            if hospital == curr.to_dict()['hospital_name']:
                userDoc = dbUser.document(curr.id).get()
                filteredDoctors.append({str(curr.id):mergeDocsToDict(userDoc, curr)})

        if len(filteredDoctors) > 0:
            return jsonify(filteredDoctors), 200
        else:
            return f"No Doctors Found at {hospital}", 200

    except Exception:
        return jsonify(f'Exception occured at filterByHospital',Exception), 401