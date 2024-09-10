import cv2
# from new_datadase import data
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("try_project\p11_facerecog\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://face-recog-and-attendence-default-rtdb.firebaseio.com/"
})

data = {}
ref = db.reference("students")
def take_photo():
    print("====be still====")
    id_number = int(input("give your id_number: " ))
    name = str(input("enter your name :"))
    major = str(input("tell your major :"))
    str_year = int(input("starting year :"))
    attendence = 0
    data[f'{id_number}'] = {"name":name, "major":major, "stating year":str_year, "total attendence": attendence}
    cap = cv2.VideoCapture(0)
    ref, fram = cap.read()
    cv2.imwrite(f"try_project\p11_facerecog\images\{id_number}.png", fram)
    cap.release()


take_photo() 
print(data)
for key, values in data.items():
    ref.child(key).set(values)
#NEXT STEP IS TO ENCODE THE PHONE SO RUN THE ENCODING FILE AND ENCODE THE PHOTOS