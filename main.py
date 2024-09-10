import cv2
import pickle
import face_recognition
import numpy as np 
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
 
cred = credentials.Certificate("try_project\p11_facerecog\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://face-recog-and-attendence-default-rtdb.firebaseio.com/",
    "storageBucket":"face-recog-and-attendence.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
# bg= cv2.imread()

# starting to tracke the face 
print("Loadinh Encoding File...")
file = open("try_project\p11_facerecog\encodingFile.p",'rb')
encoderlistwithid = pickle.load(file)#bringing the encoded file 
file.close()
encoderLIstKnow, studentlist = encoderlistwithid
# print(studentlist)
print("All Done")

modeType = 0
counter = 0
id = -1
imgstudent = []
while True:
    success, img = cap.read()
    imgs = cv2.resize(img,(0,0), None,0.25,0.25)#resizing the scale of the image for faster computation
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
    facerecog = face_recognition.face_locations(imgs)
    encodecurrimg = face_recognition.face_encodings(imgs, facerecog)
    for encodface, facelock in zip(encodecurrimg, facerecog):
        face_campare = face_recognition.compare_faces(encoderLIstKnow, encodface)#face match accuracy will giving by thing where lesser the match more the good match
        facedis = face_recognition.face_distance(encoderLIstKnow, encodface)
        # print(face_campare)
        # print(facedis)        
        matchindex = np.argmin(facedis)
        # print("hey it you",matchindex)
        if face_campare[matchindex]:
            # print("it you")
            # print(studentlist[matchindex])
            y1, x2, y2, x1 = facelock#some problem in geometry need to get fix 
            y1, x2, y2, x1= y1*4, x2*4, y2*4, x1*2#some problem in geometry need to get fix 
            bbox = 90 + x1, 120 + y1, x2-x1, y2-y1#some problem in geometry need to get fix 
            rect = cvzone.cornerRect(img, bbox, rt = 0)#some problem in geometry need to get fix 
            id  = studentlist[matchindex]
            if counter ==0:
                counter = 1
                modeType = 1
                
    if counter!=0:
        if counter ==1:
            studentinfo = db.reference(f"students/{id}").get()#getting the data
            #updating the data of attendence 
            ref = db.reference(f'students/{id}')
            studentinfo['total attendence'] +=1
            ref.child('total attendence').set(studentinfo['total attendence'])
            # print(studentinfo) 
            print("student name: ",studentinfo["name"])
            print("student name: ",studentinfo["major"])    
            print("students attendence: ",studentinfo["total attendence"]) 
             
# ====================================================================================================================================
# will not includ this part as its just the back end.!!
            #getting the image of the right person
            # blob = bucket.get_blob(f'{id}.png')
            # arry = np.frombuffer(blob.download_as_string(),np.unit8)
            # imgstudent  = cv2.imdecode(arry, cv2.COLOR_BGRA2BGR )   
# ====================================================================================================================================
        counter+=1 
        
    cv2.imshow("face", img)
    # cv2.imshow("recog", imgstudent)
    cv2.waitKey(1)
   