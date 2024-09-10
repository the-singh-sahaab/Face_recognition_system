import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("try_project\p11_facerecog\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://face-recog-and-attendence-default-rtdb.firebaseio.com/"
})

ref = db.reference("students")
data = {
    "342":
    {
        "name": "shubham Singh",
        "major": "computer scince",
        "stating year": 2021,
        "total attendence": 6
        },
    "1243245":
    {
        "name": " Singh",
        "major": "computer ",
        "stating year": 2020,
        "total attendence": 5
        },
    
}

for key, values in data.items():
    ref.child(key).set(values)