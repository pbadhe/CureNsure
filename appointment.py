import notify, uuid, convertTime
from flask import jsonify

def scheduleAppointment(db, request):
    try:
        apt_id = request.json["appointment_id"]
        db_apt_doc = db.collection(u'Appointment').document(apt_id)
        aptDict = db_apt_doc.get().to_dict()

        if "patient_user_id" in aptDict:
            return jsonify({"Error": "This slot has already been scheduled"}), 401  

        aptDict["patient_user_id"] = request.json["patient_user_id"]
        aptDict["note"] = request.json.get("note", "") #Optional so can be empty
        aptDict["type"] = request.json["type"]

        db_apt_doc.update(aptDict)

        #Total available beds are decreased by 1 if beds are needed (Questionnaire)
        if "needs_bed" in request.json:
            d1 = db.collection('Doctor').document(aptDict["doc_user_id"])
            docDict = d1.get().to_dict()
            if "supports_covid" not in docDict:
                return jsonify({"Error": "The doctor doesn't support covid treatment"}), 401  
            else:
                docDict["supports_covid"] -= 1
            d1.update(docDict)
        #Send email notification
        message = """\
Subject: CureNsure Appointment Scheduled 

This message is sent from CureNsure."""
        destEmail = db.collection('User').document(request.json["patient_user_id"]).get().to_dict().get("user_email")
        notify.sendEmail(destEmail, message)
        return jsonify({"Slot_Scheduled": True, "appointment_id": apt_id}), 200

    except Exception as e:
        return jsonify({"Slot_Scheduled": False, "appointment_id": apt_id, "Error":e}), 401        

def addDoctorSlot(db, request):
    try:
        slot_data = {
            u'doc_user_id': request.json["doc_user_id"],
            u'time': convertTime.convertToDbObject(request.json['time']),
            u'note': request.json.get("note", "") #Optional so can be empty
        }
        apt_id = str(uuid.uuid4())[:8]
        db.collection(u'Appointment').document(apt_id).set(slot_data)
        return jsonify({"Slot_Added": True, "appointment_id": apt_id}), 200

    except Exception as e:
        return jsonify({"Slot_Added": False,"Error":e}), 401

def upcomingUserApts(db, request):
    apts = []
    id = request.json["patient_user_id"]
    query = db.collection('Appointment').where("patient_user_id", "==", id)
    for apt in query.stream():
        d1 = apt.to_dict()
        x = convertTime.convertToString(d1["time"])
        d1["time"] = x
        if convertTime.upcoming(x):
            apts.append({str(apt.id):d1})
    
    if len(apts) > 0:
        return jsonify(apts), 200
    else:
        return f"No appointments found for patient_user_id {id}", 200


def viewPatientApts(db, request):
    apts = []
    id = request.json["patient_user_id"]
    query = db.collection('Appointment').where("patient_user_id", "==", id)
    for apt in query.stream():
        d1 = apt.to_dict()
        d1["time"]  = convertTime.convertToString(d1["time"])
        apts.append({str(apt.id):d1})
    
    if len(apts) > 0:
        return jsonify(apts), 200
    else:
        return f"No appointments found for patient_user_id {id}", 200

#indicator: 0 -> appointments, 1 -> slots, 3-> upcoming appointments
def viewDocApts(db, request, indicator):
    apts = []
    id = request.json["doc_user_id"]
    query = db.collection('Appointment').where("doc_user_id", "==", id)
    for apt in query.stream():
        d1 = apt.to_dict()
        d1["time"] = convertTime.convertToString(d1["time"])
        x = d1["time"]
        #After appointment is scheduled, type field exists in the record. 
        #Before that it is just a slot.
        if ((indicator == 3 and convertTime.upcoming(x)) or indicator == 0) and "type" in d1:
            apts.append({str(apt.id):d1})
        elif indicator == 1 and "type" not in d1:
            apts.append({str(apt.id):d1})
    
    if len(apts) > 0:
        return jsonify(apts), 200
    else:
        return f"No appointments found for doc_user_id {id}", 200

def update_supports_covid_beds(db, request):
    try:
        id = request.json["doc_user_id"]
        doc = db.collection('Doctor').document(id)
        docDict = doc.get().to_dict()
        if "supports_covid" not in docDict:
            return jsonify({"Error": "The doctor doesn't support covid treatment"}), 401  
        else:
            docDict["supports_covid"] = request.json["supports_covid"]
        
        print("here")
        doc.update(docDict)

    except Exception as e:
        return jsonify(e), 401

    return jsonify({"Status": "TotalBedsUpdated"}), 200  