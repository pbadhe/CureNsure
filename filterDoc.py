from tokenize import Special
from flask import jsonify

def mergeDocs(doc1, doc2):
    return dict(list(doc1.to_dict().items()) + list(doc2.to_dict().items()))

def filterDocByName(db, request):
    first_name = request.json.get('first_name', ' ') #space; bcz comparing with '' below if no value exists 
    last_name = request.json.get('last_name', ' ')
    
    try:
        dbDoc = db.collection('Doctor')
        dbUser = db.collection('User')
        docFiltered = []
        for doc in dbDoc.stream():
            user = dbUser.document(doc.id).get()
            if user:
                first = user.to_dict().get('first_name','')
                last =  user.to_dict().get('last_name','')
                if first == first_name or last == last_name:
                    docFiltered.append(f'\'{doc.id}\':{mergeDocs(doc,user)}')
                
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
            if "1" == curr.to_dict().get('supports_covid',''):
                userDoc = dbUser.document(curr.id).get()
                filteredDoctors.append(f'\'{curr.id}\':{mergeDocs(userDoc, curr)}')

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
                filteredDoctors.append(f'\'{curr.id}\':{mergeDocs(userDoc, curr)}')

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
                filteredDoctors.append(f'\'{curr.id}\':{mergeDocs(userDoc, curr)}')

        if len(filteredDoctors) > 0:
            return jsonify(filteredDoctors), 200
        else:
            return f"No Doctors Found at {hospital}", 200

    except Exception:
        return jsonify(f'Exception occured at filterByHospital',Exception), 401