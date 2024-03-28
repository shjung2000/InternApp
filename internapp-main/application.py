from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from itsdangerous import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/application'
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/application'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}


db = SQLAlchemy(app)
CORS(app)


class Application(db.Model):
    __tablename__ = 'application'

    applicationID = db.Column(db.Integer, primary_key = True)
    companyID = db.Column(db.ForeignKey('company.companyID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    studentID = db.Column(db.ForeignKey('student.studentID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    jobID = db.Column(db.ForeignKey('job.jobID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    coverletter = db.Column(db.String(1000), nullable = False)
    applicationStatus = db.Column(db.String(20), nullable = False)
    
    company = db.relationship(
        'Company', primaryjoin='Application.companyID == Company.companyID', backref='application')
    
    student = db.relationship(
        'Student', primaryjoin='Application.studentID == Student.studentID', backref='application')

    job = db.relationship(
        'Job', primaryjoin='Application.jobID == Job.jobID', backref='application')

    def __init__(self, applicationID, companyID, studentID, jobID, coverletter, applicationStatus):
        self.applicationID = applicationID
        self.companyID = companyID
        self.studentID = studentID
        self.jobID = jobID
        self.coverletter = coverletter
        self.applicationStatus = applicationStatus

    def json(self):
        return {
            "applicationID": self.applicationID,
            "companyID": self.companyID,
            "studentID": self.studentID,
            "jobID": self.jobID,
            "coverletter": self.coverletter,
            "applicationStatus": self.applicationStatus,
        }

class Company(db.Model):
    __tablename__ = 'company'

    companyID = db.Column(db.Integer, primary_key = True)
    companyName = db.Column (db.String(100), nullable=False)
    companyDesc = db.Column(db.String(100), nullable=False)
    companySize = db.Column(db.Integer)

    def __init__(self, companyID, companyName, companyDesc, companySize):
        self.companyID = companyID
        self.companyName = companyName
        self.companyDesc = companyDesc
        self.companySize = companySize

    def json(self):
        return {
            "companyID": self.companyID,
            "companyName": self.companyName,
            "companyDesc": self.companyDesc,
            "companySize": self.companySize
        }

class Student(db.Model):
    __tablename__ = 'student'

    studentID = db.Column(db.Integer, primary_key = True)
    studentName = db.Column (db.String(100), nullable=False)
    studentEmail = db.Column(db.String(100), nullable=False)
    phoneNum = db.Column(db.Integer)
    

    def __init__(self, studentID, studentName, studentEmail, phoneNum, resume):
        self.studentID = studentID
        self.studentName = studentName
        self.studentEmail = studentEmail
        self.phoneNum = phoneNum
        

    def json(self):
        return {
            "studentID": self.studentID,
            "studentName": self.studentName,
            "studentEmail": self.studentEmail,
            "phoneNum": self.phoneNum,
            
        }

class Job(db.Model):
    __tablename__ = 'job'

    companyID = db.Column(db.ForeignKey('company.companyID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    jobID = db.Column(db.Integer, primary_key = True)
    jobName = db.Column(db.String(100), nullable = False)
    postDate = db.Column(db.DateTime, nullable = False)
    jobDesc = db.Column(db.String(1000), nullable = False)
    deadline = db.Column(db.DateTime, nullable = False)

    company = db.relationship(
        'Company', primaryjoin='Job.companyID == Company.companyID', backref='job')

    def __init__(self, companyID, companyName, companyDesc, companySize, jobID, jobName, postDate, jobDesc, deadline):
        self.companyID = companyID
        self.companyName = companyName
        self.companyDesc = companyDesc
        self.companySize = companySize
        self.jobID = jobID
        self.jobName = jobName
        self.postDate = postDate
        self.jobDesc = jobDesc
        self.deadline = deadline

    def json(self):
        return {
            "companyID": self.companyID,
            "companyName": self.companyName,
            "companyDesc": self.companyDesc,
            "companySize": self.companySize,
            "jobID": self.jobID,
            "jobName": self.jobName,
            "postDate": self.postDate,
            "jobDesc": self.jobDesc,
            "deadline": self.deadline
        }


#testing
@app.route("/applications")
def index():
    return "this is application page"

#Get All Applications
@app.route("/application")
def get_all():
    applicationList = Application.query.all()
    if len(applicationList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobs": [application.json() for application in applicationList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no applications."
        }
    ), 404

#Get all applications of a particular student
@app.route("/application/<int:studentID>")
def get_all_by_student(studentID):
    applicationList = Application.query.filter_by(studentID = studentID).all()
    if len(applicationList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "applications": [application.json() for application in applicationList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "This student did not apply for any jobs"
        }
    ), 404 


#Checking if the student hasn't applied -> student is able to apply 
@app.route("/application_check/<int:applicationID>")
def cross_check(applicationID):
    
    applicant = Application.query.filter_by(applicationID = applicationID).first()
    
    if applicant:
        return jsonify(
            {
                "code": 404,
                "message": "The applicant already applied for this job."
            }
        )
    return jsonify(
        {
            "code": 200 ,
            "message" : "The applicant is able to apply for this job."
        }
    )
    

#check_if_applicant_exist_in_database
@app.route("/application/exist/<int:applicationID>")
def check_exist(applicationID):
    applicant = Application.query.filter_by(applicationID = applicationID).first()
    if applicant:
        return jsonify(
            {
                "code":200,
                "message": "Applicant exists in the database!"
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Applicant does not exist in the database!"
        }
    ), 404 


#search for specific applicant
@app.route("/application/<int:applicationID>")
def find_by_applicationID(applicationID):
    applicant = Application.query.filter_by(applicationID = applicationID).first()
    if applicant:
        return jsonify(
            {
                "code": 200,
                "data": applicant.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Applicant searched does not exist."
        }
    ), 404 

#Create new applicant 
@app.route("/application/<int:applicationID>" , methods = ['POST'])
def createApplicant(applicationID):

    
    companyID = request.json.get('companyID' , None)
    studentID = request.json.get('studentID' , None)
    jobID = request.json.get('jobID' , None)
    coverletter = request.json.get('coverletter' , None)

    new_applicant = Application(applicationID = applicationID, companyID = companyID , studentID = studentID , jobID = jobID , coverletter = coverletter , applicationStatus = 'pending')

    

    try:
        db.session.add(new_applicant)
        db.session.commit()
    
    except Exception as e:
        print(e)
        return jsonify({
            "code": 500,
            "data": {
                "applicationID": applicationID
            },
            "message": "An error occurred creating new application"
        }), 500

    return jsonify(
        {
            "code": 201,
            "data": new_applicant.json(),
            "message1": "You have submitted your application",
            "message2": "Received an application"
        }
    ), 201 

#Update application Status
@app.route("/application/<int:applicationID>", methods = ["PUT"])
def update_status(applicationID):
    data = request.get_json()
    applicant = Application.query.filter_by(applicationID = applicationID).first()
    if applicant:
        if data['applicationStatus']:
            applicant.applicationStatus = data['applicationStatus']

            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "message": "Update successful!"
                }
            )

    else:
        return jsonify(
            {
                "code": 404,
                "message": "Applicant does not exist"
            }
        )
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)