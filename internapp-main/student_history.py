#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from time import strftime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from io import StringIO
from email import message
import json
import os
from datetime import datetime
from os import environ
import amqp_setup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/record_one'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)
class studentHistory(db.Model):
    __tablename__ = 'record_one'
    
    jobName = db.Column(db.String(100), primary_key = True)
    companyName = db.Column(db.String(100), nullable = False)
    message = db.Column(db.String(100) , nullable = False)
    time = db.Column(db.String(100), nullable=False)

    def __init__(self, jobName , companyName , message , time):
        self.jobName = jobName
        self.companyName = companyName
        self.message = message
        self.time = time

    def json(self):
        return {
            "jobName": self.jobName,
            "companyName": self.companyName,
            "message": self.message,
            "time": self.time
        }



monitorBindingKey='*.student'

def receiveStudent():
    amqp_setup.check_setup()
    
    queue_name = 'Student_notification'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

    


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an error by " + __file__)
    processStudent(body)
    print() # print a new line feed

def processStudent(StudentMsg):
    print("Printing the application message for student UI:")
    try:
        message = json.loads(StudentMsg)
        print(type(message))
        messageReceived = message["message"]
        jobName = message["jobName"]
        companyName = message["companyName"]
        now=datetime.now()
        current_time = str(now)

        
        print(messageReceived)
        print(jobName)
        print(companyName)

        new_record = studentHistory(jobName = jobName , companyName = companyName ,  message = messageReceived , time = current_time)

        try:
            db.session.add(new_record)
            db.session.commit()

        except Exception as e:
            print(e)
            return jsonify({
                "code": 500,
                "message": "An error occurred creating new application"
            }), 500  

    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", StudentMsg)
    print()

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
    
if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveStudent()
