import datetime

def convertToString(dbDateObject):
    year,month,day,hour,minute,second = dbDateObject.year,dbDateObject.month,dbDateObject.day,dbDateObject.hour, dbDateObject.minute, dbDateObject.second
    utc_time  = "%s-%s-%sT%s:%s:%s"%(year, month, day,hour,minute,second)
    return utc_time

def convertToDbObject(dateString):
    # (Firebase-> 
    #       Default timezone UTC
    #       Default offset UTC -5H (Regional) => %z should match +HHMM or -HHMM 
    format_data = '%Y-%m-%dT%H:%M:%S.%z'
    dateString += ".-0500" 
    return datetime.datetime.strptime(dateString, format_data)
    # Daylight savings TIME OFFSET issues in the long term if maintaining the repo :D

def upcoming(x):
    cx = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S')
    cNow = datetime.datetime.strptime(convertToString(datetime.datetime.now()), '%Y-%m-%dT%H:%M:%S')
    print(cx, "here", cNow)
    print(cx > cNow)
    return (cx > cNow)