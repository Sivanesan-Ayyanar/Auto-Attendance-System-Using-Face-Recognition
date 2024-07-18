import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://autoattendance-763d3-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "21226":
        {
            "name": "Priyadharshan",
            "major": "BE RAE",
            "year": 3,
            "starting_year": 2021,
            "College": "PSGCT",
            "total_attendance": 0,
            "last_attendance_time": "2024-03-08 00:54:34"
        },
    "21242":
        {
            "name": "Sivanesan",
            "major": "BE RAE",
            "year": 3,
            "starting_year": 2021,
            "College": "PSGCT",
            "total_attendance": 0,
            "last_attendance_time": "2024-03-08 00:54:34"
        },
    "21218":
        {
            "name": "JaiSurya",
            "major": "BE RAE",
            "year": 3,
            "starting_year": 2021,
            "College": "PSGCT",
            "total_attendance": 0,
            "last_attendance_time": "2024-03-08 00:54:34"
        },
    "21211":
        {
            "name": "Dhanush",
            "major": "BE RAE",
            "year": 3,
            "starting_year": 2021,
            "College": "PSGCT",
            "total_attendance": 0,
            "last_attendance_time": "2024-03-08 00:54:34"
        },

}
for key, value in data.items():
    ref.child(key).set(value)