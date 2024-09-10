import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
 
cred = credentials.Certificate("try_project\p11_facerecog\serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://face-recog-and-attendence-default-rtdb.firebaseio.com/",
    "storageBucket":"face-recog-and-attendence.appspot.com"
})


folderpath = 'try_project\p11_facerecog\images'
pathlist = os.listdir(folderpath)
# print(pathlist)
imglist = []
studentlist = []
for i in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath, i)))
    studentlist.append(os.path.splitext(i)[0])
    print(studentlist)
    fileName = f'{folderpath}\{i}' 
    Bucket = storage.bucket()
    blob = Bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
    

# here we will encode the image 
def encodeing(imageslist):
    encodedlist = []
    
    for im in imageslist:
        #   first step is to change ghe color of the image to rbg
        img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # encodeing the image 
        encode = face_recognition.face_encodings(img)[0]
        # make a list of the encoded image
        encodedlist.append(encode)
    return encodedlist  
imageslist = imglist
print("encodinh started .... ")
encoderLIstKnow = encodeing(imageslist) 
encoderlistwithid = [encoderLIstKnow, studentlist]
print("encoding is done!")
        
        
file  = open('try_project\p11_facerecog\encodingFile.p','wb')
pickle.dump(encoderlistwithid, file)
file.close
print("....saved")
