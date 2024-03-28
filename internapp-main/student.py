from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/student'
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/student'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)
class Student(db.Model):
    __tablename__ = 'student'

    studentID = db.Column(db.Integer, primary_key = True)
    studentUsername = db.Column (db.String(100), nullable=False)
    studentName = db.Column (db.String(100), nullable=False)
    studentEmail = db.Column(db.String(100), nullable=False)
    phoneNum = db.Column(db.Integer)
    studentPassword = db.Column(db.String(1000), nullable=False)
    
    def __init__(self, studentID, studentUsername, studentName, studentEmail, phoneNum, studentPassword):
        self.studentID = studentID
        self.studentUsername = studentUsername
        self.studentName = studentName
        self.studentEmail = studentEmail
        self.phoneNum = phoneNum
        self.studentPassword = studentPassword
        

    def json(self):
        return {
            "studentID": self.studentID,
            "studentUsername": self.studentUsername,
            "studentName": self.studentName,
            "studentEmail": self.studentEmail,
            "phoneNum": self.phoneNum,
            "studentPassword": self.studentPassword,
        }
    

# retrieve all students profile
@app.route("/student")
def get_all():
    students = Student.query.all()
    if len(students):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "students": [student.json() for student in students]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no students in the database."
        }
    ), 404


#For cross checking student identity
@app.route("/student_check")
def cross_check():
    studentID = request.json.get("studentID" , None)

    student = Student.query.filter_by(studentID = studentID).first()
    if student:
        return jsonify(
            {
                "code": 200,
                "data": student.json()
            },
            
        )
    return jsonify(
        {
            "code": 404,
            "message" : "Such student does not exist."
        }
    )

#retrieve a specific student details
@app.route("/student/<int:studentID>")
def find_by_studentID(studentID):
    student = Student.query.filter_by(studentID = studentID).first()
    if student:
        return jsonify(
            {
                "code": 200,
                "data": student.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No such student exists."
        }
    )

# create new student profile
@app.route("/student/<int:studentID>", methods=['POST'])
def create_student(studentID):
    data = request.get_json()
    if (Student.query.filter_by(studentID=studentID).first()) or (Student.query.filter_by(studentUsername=data["studentUsername"]).first()):
        return jsonify({
            "code": 400,
            "data": {
                "studentID": studentID
            },
            "message": "Student already exists."
        }), 400

    
    student = Student(studentID, **data)

    try:
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "code": 500,
            "data": {
                "studentID": studentID
            },
            "message": "An error occurred creating the student's profile"
        }), 500

    return jsonify(
        {
            "code": 201,
            "data": student.json()
        }
    ), 201


# update student profile
@app.route("/student/<int:studentID>", methods=['PUT'])
def update_student(studentID):
    student = Student.query.filter_by(studentID=studentID).first()
    if student:
        data = request.get_json()
        if data['studentName']:
            student.studentName = data['studentName']
        if data['studentEmail']:
            student.studentEmail = data['studentEmail']
        if data['phoneNum']:
            student.phoneNum = data['phoneNum']
        if data['studentPassword']:
            student.studentPassword = data['studentPassword']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": student.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "studentID": studentID
            },
            "message": "Student not found."
        }
    ), 404

# delete application
@app.route("/student/<int:studentID>", methods=['DELETE'])
def delete_student(studentID):
    student = Student.query.filter_by(studentID=studentID).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "studentID": studentID
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "studentID": studentID
            },
            "message": "Student not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
    