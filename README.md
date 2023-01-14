# CureNsure

CureNsure is a flask based Patient & Healthcare/Insurance Management Platform providing REST APIs for following features:

1. Appointment scheduling and management.
2. Insurance plan selection and recommendation.
3. Secure messaging and encryption.
4. Tracking status & COVID-19 supportive features.

## Developed By
- Pranav Badhe (badhepranav@gmail.com)
- Oleg Lyashchuk

 For concerns or suggestions, contact on the given email address.

## Installation

1. Clone CureNsure [repository](https://github.iu.edu/pbadhe/CureNsure).
2. Create a firestore database for supporting data operations.
3. Make sure you have the firestore secret key json file stored in the default [location](https://github.com/pbadhe/CureNsure/tree/main/credentials).
4. If deployment is necessary, make sure you have the firestore database linked to the Google Cloud project which you want to host to the Cloud Run with
appropriate [IAM permissions](https://cloud.google.com/run/docs/reference/iam/roles).
5. Install all the required packages using package manager [pip](https://pip.pypa.io/en/stable/) with command ```pip install -r
requirements.txt``` in the working environment. 
6. Run the flask server by executing ```python cure.py``` to host the application
and serve the APIs.
7. For testing the APIs, Postman application can be installed. To install Postman, visit this [link](https://www.postman.com/downloads/).

## Usage

To setup the database, see the [resource documents](https://github.com/pbadhe/CureNsure/tree/main/resourceDocs) and use the file [```createSchema.py```](https://github.com/pbadhe/CureNsure/blob/main/createSchema.py) for schema creation. Routes for all the APIs can be found in [```cure.py```](https://github.com/pbadhe/CureNsure/blob/main/cure.py) with appropriate documentation. APIs can be tested by importing the example-ready, labelled [Postman API collection](https://github.com/pbadhe/CureNsure/blob/main/FlaskREST/Localhost.postman_collection.json) into the Postman Client. For more information on importing a json collection, visit [here](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#converting-postman-collections-from-v1-to-v2). The postman collection has all the API requests labelled with sample request and response.

For example, a simple GET request for searching details of a doctor whose ```id``` is known can be called in the following way: (Flask server's default port is 8080 when hosted locally)
#### Request

`GET /list`

    http://localhost:8080/list?id=3f4acd25

#### Response

    HTTP/1.1 200 OK
    Server: Werkzeug/2.2.2 Python/3.10.8
    Date: Fri, 09 Dec 2022 04:24:16 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 311
    Access-Control-Allow-Origin: *

    {"hospital_name": "IU Health Center in Absolute Demo!", "id": "3f4acd25",
     "role_id": "2", "speciality": "Physician", "user_address": "Bloomington, IN",
     "user_email": "oleg@iu.edu", "user_first_name": "Joe", "user_gender": "Male",
     "user_last_name": "Nani", "user_mobile": "123134234", "user_name": "idkas", 
     "user_zipcode": "23466433" }

## Deployment

Files [```cloudbuild.yaml```](https://github.com/pbadhe/CureNsure/blob/main/cloudbuild.yaml) and [```Dockerfile```](https://github.com/pbadhe/CureNsure/blob/main/Dockerfile) can be used during deployment of containerized code. For more information on deployment to Google cloud, visit [here](https://codelabs.developers.google.com/codelabs/cloud-run-deploy#2).


## Contributing

Pull requests or any suggestions are welcome. Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

