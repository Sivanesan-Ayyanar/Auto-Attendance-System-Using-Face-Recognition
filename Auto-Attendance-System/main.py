import os
import pickle
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://autoattendance-763d3-default-rtdb.firebaseio.com/Q",
    'storageBucket': "autoattendance-763d3.appspot.com"
})
bucket = storage.bucket()
img = cv2.VideoCapture(0)
img.set(3, 640)   # setting the width of webcam
img.set(4, 480)   # setting height of webcam
if not img.isOpened():
    print("Error: Could not open camera.")
    exit()
imgBackground = cv2.imread('GUI_files/C.png')
# Importing the mode images into a list
folderModePath = r"C:\IEEE paper\faceRecognitionRealTime\FACE_APP\GUI_files\Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# Load the encoding file
print("Loading Encode File ...")
file = open(r"C:\IEEE paper\faceRecognitionRealTime\FACE_APP\EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")
modeType = 0
counter = 0
id = -1
imgStudent = []
folderPath = 'GUI_files/Modes'
pathList = os.listdir(folderPath)
print(pathList)
attendance_status = {student_id: False for student_id in studentIds}  # Initialize attendance status
for path in pathList:
    student_id = os.path.splitext(path)[0]
    attendance_status[student_id] = False  # Initialize each student as absent

while True:

    success, frame = img.read()

    imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = frame
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if encodeCurFrame:  # Check if any face is detected
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                id = studentIds[matchIndex]
                if not attendance_status[id]:
                    attendance_status[id] = True  # Mark the student as present

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                color = (0, 255, 0)  # Green color in BGR format
                thickness = 2  # Fill the square

                imgBackground = cv2.rectangle(imgBackground, (x1 + 55, y1 + 162), (x2 + 55, y2 + 162), color, thickness)
                id = studentIds[matchIndex]
                if counter == 0:
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                imgStudent = cv2.imread(f"C:/IEEE paper/faceRecognitionRealTime/FACE_APP/Students_Images/{id}.png")
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                if secondsElapsed > 60:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 2
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)  # Set color to dark
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)  # Set color to dark
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)  # Set color to dark
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)  # Set color to dark

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                    cv2.waitKey(10)
                    #imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            if modeType ==30:
                if 10 < counter < 20:
                    modeType = 2
                    cv2.waitKey(1)
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
                counter += 1
                if counter >= 2:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
    if cv2.waitKey(10) & 0xFF == 27:  # 27 is the ASCII code for the 'Escape' key
        break
img.release()
cv2.destroyAllWindows()
# Generate and print attendance report
presentees = [student_id for student_id, present in attendance_status.items() if present]
absentees = [student_id for student_id, present in attendance_status.items() if not present]
print("Presentees:")
for student_id in presentees:
    print(f"Student ID: {student_id}")
print("\nAbsentees:")
for student_id in absentees:
    print(f"Student ID: {student_id}")
