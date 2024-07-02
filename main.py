import cv2
import numpy as np
import face_recognition
import os
from operations import *
from datetime import datetime
from add_face import *

def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def take_attendance():
    path = 'images'
    images = []
    personNames = []
    myList = os.listdir(path)
    print(myList)
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personNames.append(os.path.splitext(cu_img)[0])
    print(personNames)
    encodeListKnown = faceEncodings(images)
    print('All Encodings Complete!!!')
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personNames[matchIndex]
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                write_attendance_in_xl(name, get_dict())
        cv2.imshow('Taking attendance', frame)
        if cv2.waitKey(1) == 13:
            break
    cap.release()
    cv2.destroyAllWindows()
    return

while True:
    print('Press 1 to take attendance')
    print('Press 2 to add new face')
    print('Press 3 to exit')
    choice = input('Enter your choice: ')
    if choice == "1":
        take_attendance()
    elif choice == "2":
        password= input('Enter password: ')
        if password == '12345':
            add_the_face()
        else:
            print('Wrong password')
    elif choice == "3":
        break
    else:
        print('Invalid choice')