#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
from datetime import datetime
from os import environ
import amqp_setup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/history_one'
#app.config['SQLALCHEMY_DATABASE_URI'] =  environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/history_one'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)
class companyHistory(db.Model):
    __tablename__ = 'history_one'
    
    jobName = db.Column(db.String(100), primary_key = True)
    studentName = db.Column(db.String(100), nullable = False)
    message = db.Column(db.String(100) , nullable = False)
    time = db.Column(db.String(100), nullable=False)

    def __init__(self, jobName , studentName , message , time):
        self.jobName = jobName
        self.studentName = studentName
        self.message = message
        self.time = time

    def json(self):
        return {
            "jobName": self.jobName,
            "studentName": self.studentName,
            "message": self.message,
            "time": self.time
        }

monitorBindingKey='*.company'

def receiveCompany():
    amqp_setup.check_setup()
    
    queue_name = 'Company_notification'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an error by " + __file__)
    processCompany(body)
    print() # print a new line feed

def processCompany(CompanyMsg):
    print("Printing the application message for company UI:")
    try:
        message = json.loads(CompanyMsg)
        print(type(message))
        messageReceived = message["message"]
        jobName = message["jobName"]
        studentName = message["studentName"]
        now=datetime.now()
        current_time = str(now)

        
        print(messageReceived)
        print(jobName)
        print(studentName)

        new_record = companyHistory(jobName = jobName , studentName = studentName ,  message = messageReceived , time = current_time)

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
        print("--DATA:", CompanyMsg)
    print()


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveCompany()
