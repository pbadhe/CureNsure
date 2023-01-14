from flask import jsonify
import uuid, notify

def setIPlan(db,request):
    try:
        db_user_doc = db.collection(u'User').document(request.json['patient_user_id'])
        userDict = db_user_doc.get().to_dict()
        userDict['plan_id']=request.json['plan_id']

        db_plan_doc = db.collection(u'IPlan').document(userDict['plan_id'])
        premium = db_plan_doc.get().to_dict()['monthly_premium']

        x = userDict.get('total_contributed_amount',[])
        if not x:
            userDict['total_contributed_amount'] = [premium, premium]
        else:
            premium = int(premium[1:])
            v = x[0]
            v = "$" + str(int(v[1:]) + premium)
            userDict['total_contributed_amount'] = [v, "$" + str(premium)]

        db_user_doc.update(userDict)
        message = """\
Subject: CureNsure Insurance Plan Updated

This message is sent from CureNsure."""
        notify.sendEmail(userDict['user_email'], message)
        return jsonify({"Plan_Set": True, "plan_id": request.json['plan_id']}), 200
    except Exception as e:
        return jsonify({"Plan_Set": False, "plan_id": request.json['plan_id'], "Error":e}), 401        
    
def addIPlan(db, request):
    try:
        slot_data = {
            u'agent_user_id': request.json["agent_user_id"],
            u'plan_type': request.json["plan_type"], #(bronze,gold,diamond)
		    u'monthly_premium': request.json["monthly_premium"]
        }
        plan_id = str(uuid.uuid4())[:8]
        db.collection(u'IPlan').document(plan_id).set(slot_data)
        return jsonify({"Plan_Added": True, "plan_id": plan_id}), 200
    except Exception as e:
        return jsonify({"Plan_Added": False,"Error":e}), 401     

def updateIPlan(db, request):
    try:
        plan_id = request.json['plan_id']
        db_plan_doc = db.collection(u'IPlan').document(plan_id)
        planDict = db_plan_doc.get().to_dict()
        planDict['plan_type']=request.json['plan_type']
        planDict['monthly_premium']=request.json['monthly_premium']
        db_plan_doc.update(planDict)
        message = """\
Subject: CureNsure Insurance Plan Updated

This message is sent from CureNsure."""

        query = db.collection('User').where("plan_id", "==", plan_id)
        for apt in query.stream():
            destEmail = apt.to_dict().get("user_email")
            notify.sendEmail(destEmail, message)
        return jsonify({"Plan_Updated": True, "plan_id": plan_id}), 200
    except Exception as e:
        return jsonify({"Plan_Updated": False,"Error":e}), 401     

def viewAgentPlans(db,request):
    plans = []
    id = request.json.get("agent_user_id","")
    if id=="":
        try:
            dbDoc = db.collection('IPlan')
            for doc in dbDoc.stream():
                plans.append(doc.to_dict())
            return jsonify(plans), 200
        except Exception:
            return jsonify(f'Exception occured at view Plans',Exception), 401
    else:
        query = db.collection('IPlan').where("agent_user_id", "==", id)
        for plan in query.stream():
            plans.append(plan.to_dict())
        if len(plans) > 0:
            return jsonify(plans), 200
        else:
            return f"No health insurance plans found for agent_user_id {id}", 200

#Recurring amount itself is the last payment done! :)
def get_total_and_recurring_bills(db, request):
    db_user_doc = db.collection(u'User').document(request.json['patient_user_id'])
    userDict = db_user_doc.get().to_dict()
    return jsonify({"Total_Billed_Amount": userDict['total_contributed_amount'][0], "Recurring_Amount": userDict['total_contributed_amount'][1]}), 200