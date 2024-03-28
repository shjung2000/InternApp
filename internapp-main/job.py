from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from itsdangerous import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/job'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class Job(db.Model):
    __tablename__ = 'job'

    jobID = db.Column(db.Integer, primary_key = True)
    companyID = db.Column(db.ForeignKey('company.companyID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    jobName = db.Column(db.String(100), nullable = False)
    postDate = db.Column(db.DateTime, nullable = False)
    jobDesc = db.Column(db.String(1000), nullable = False)
    deadline = db.Column(db.DateTime, nullable = False)

    company = db.relationship(
        'Company', primaryjoin='Job.companyID == Company.companyID', backref='job')

    def __init__(self, jobID, companyID, jobName, postDate, jobDesc, deadline):
        self.jobID = jobID
        self.companyID = companyID
        self.jobName = jobName
        self.postDate = postDate
        self.jobDesc = jobDesc
        self.deadline = deadline

    def json(self):
        return {
            "jobID": self.jobID,
            "companyID": self.companyID,
            "jobName": self.jobName,
            "postDate": self.postDate,
            "jobDesc": self.jobDesc,
            "deadline": self.deadline
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

# get jobs
@app.route("/job")
def get_all():
    joblist = Job.query.all()
    if len(joblist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobs": [job.json() for job in joblist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no jobs."
        }
    ), 404


#cross check if job exists
@app.route("/job_check")
def job_check():
    jobID = request.json.get("jobID" , None)

    job = Job.query.filter_by(jobID = jobID).first()
    if job:
        return jsonify(
            {
                "code": 200,
                "data": job.json(),
            },
            
        )
    else:
        return jsonify(
            {
                "code": 404,
                "message": "Such job does not exist."
            }
        )

#Search for a specific Job
@app.route("/job/<int:jobID>")
def find_by_jobName(jobID):
    job = Job.query.filter_by(jobID = jobID).first()
    if job:
        return jsonify(
            {
                "code": 200,
                "data": job.json()
            } 
        )
    return jsonify(
        {
            "code": 404,
            "message": "Job searched not found."
        }
    ), 404 

# create new job posting
@app.route("/job/<int:jobID>", methods=['POST'])
def create_job(jobID):
    print("jobid: {}".format(jobID))
    if (Job.query.filter_by(jobID=jobID).first()):
        return jsonify({
            "code": 400,
            "data": {
                "jobID": jobID
            },
            "message": "Job post already exists."
        }), 400
    
    data = request.get_json()
    job = Job(jobID, **data)

    try:
        db.session.add(job)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "code": 500,
            "data": {
                "jobID": jobID
            },
            "message": "An error occurred creating the job post"
        }), 500

    return jsonify(
        {
            "code": 201,
            "data": job.json()
        }
    ), 201




# update posting
@app.route("/job/<int:jobID>", methods=['PUT'])
def update_job(jobID):
    job = Job.query.filter_by(jobID=jobID).first() #-> checking if the job exists in the database
    if job:                                        # -> if it exists then update based on the updated fields
        data = request.get_json()                  # -> jobID and companyID cannot be changed
        if data['jobName']:
            job.jobName = data['jobName']
        if data['postDate']:
            job.postDate = data['postDate']
        if data['jobDesc']:
            job.jobDesc = data['jobDesc']
        if data['deadline']:
            job.deadline = data['deadline'] 
        db.session.commit()                        #-> push the updated row into the database 
        return jsonify(
            {
                "code": 200,
                "data": job.json(),
                "message": "Job update successful!"

            }
        )
    else:                                           #-> Job does not even exist in the database 
        
        return jsonify(
        {
            "code": 404,
            "data": {
                "jobID": jobID
            },
            "message": "Job does not exist!"
        }
    ), 404



# delete posting
@app.route("/job/<int:jobID>", methods=['DELETE'])
def delete_job(jobID):
    job = Job.query.filter_by(jobID=jobID).first()
    if job:
        db.session.delete(job)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobID": jobID,
                    
                },
                "message": "Job successfully deleted!"
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "jobID": jobID
            },
            "message": "Job posting not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
    