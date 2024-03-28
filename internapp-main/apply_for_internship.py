from flask import Flask, request, jsonify
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os, sys
from os import environ
import requests

import amqp_setup
import pika
import json

from invokes import invoke_http
import random

app = Flask(__name__)
CORS(app)

applicationCheck_URL = environ.get('applicationCheck_URL') or "http://localhost:5001/application_check"
jobCheck_URL = environ.get('jobCheck_URL') or "http://localhost:5003/job_check"
studentCheck_URL = environ.get('studentCheck_URL') or "http://localhost:5004/student_check"
application_URL = environ.get('application_URL') or "http://localhost:5001/application" 
companyCheck_URL = environ.get('companyCheck_URL') or "http://localhost:5002/company_check"


#JSON Input:
#{
# companyID
#studentID 
# jobID 
#coverletter
# }

@app.route("/apply_intern" , methods = ["POST"])
def apply_intern():
    if request.is_json:
        try:
            application_detail = request.get_json()
            print("\nReceived an application detail in JSON:" , application_detail)

            result = processApplication(application_detail)
            return jsonify(result)
    

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processApplication(application_detail):
    
    check_student_exist = invoke_http(studentCheck_URL , method = 'GET' , json = application_detail)
    print("\nStudent microservice invoked")

    check_job_exist = invoke_http(jobCheck_URL , method = 'GET' , json = application_detail)
    print("\nJob microservice invoked")
    
    print(check_job_exist)

    inputJobID = application_detail["jobID"]
    inputCompanyID = application_detail["companyID"]

    databaseJobID = check_job_exist["data"]["jobID"]
    databaseCompanyID = check_job_exist["data"]["companyID"]


    student_check_code = check_student_exist["code"]
    
    print(student_check_code)
    
    
    
    
    if student_check_code == 200 and int(inputJobID) == databaseJobID and int(inputCompanyID) == databaseCompanyID:

        newId = r1 = random.randint(1, 10000)

        print(newId)

        check_applicant_can_apply = invoke_http("".join((applicationCheck_URL, "/", str(newId))) , method = 'GET' , json = application_detail)
        
        print("\nApplicant microservice invoked")

        applicant_check_code = check_applicant_can_apply["code"]

        print(applicant_check_code)


        if(applicant_check_code == 200):

            ApplicantCreation = invoke_http("".join((application_URL, "/", str(newId))) , method = 'POST' , json = application_detail)
            company_invoke=invoke_http(companyCheck_URL , method = 'GET' , json = application_detail) #this invocation is to get the companyName
            

            print(ApplicantCreation["code"])
                   
            application_message=json.dumps(ApplicantCreation)
            dict1=json.loads(application_message)
            print(dict1)
            print(type(dict1))

            
            
            
            job_message=json.dumps(check_job_exist)
            dict2=json.loads(job_message)
            print(dict2)
            print(type(dict2))

            company_message=json.dumps(company_invoke)
            dict3=json.loads(company_message)
            print(dict3)
            print(type(dict3))
                
            
            student_message=json.dumps(check_student_exist)
            dict4=json.loads(student_message)
            print(dict4)
            print(type(dict4))

            #to_be_sent = student_message["message1"]

            #For Student
            message={"message":dict1["message1"],
            "jobName":dict2["data"]["jobName"],
            "companyName":dict3["data"]["companyName"]}
    
            print(message)
            message_send_student=json.dumps(message, indent = 4)

            #for company
            message2={"message":dict1["message2"],
            "jobName":dict2["data"]["jobName"],
            "studentName":dict4["data"]["studentName"]}

            print(message2)
            message_send_company=json.dumps(message2, indent = 4)

            
            

            

            if ApplicantCreation["code"] == 201:
                
                # send email confirmation to user via Twilio
                print('\n\n-----Invoking email.py as application succeeds-----')
                
                message = Mail(from_email = 'estherrrlychee@gmail.com',
                to_emails = 'minthukha99@gmail.com',
                subject = 'Application Successful',
                plain_text_content = 'Dear User, \nKindly note that the application has been successfully created.\n\nRegards,\nPudding PTE. LTD.')
                print("aaaaaaa")
                print(Mail())
            
                
                try:
                    sg = SendGridAPIClient('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')
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)

                except Exception as e:
                    print(e)

                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="application_detail.student", 
                    body=message_send_company, properties=pika.BasicProperties(delivery_mode = 2))

                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="application_detail.company", 
                    body=message_send_student, properties=pika.BasicProperties(delivery_mode = 2)) 
                

                return {
                    
                    "message" : "Application Successful!"
                }
                

            else:

                return {
                    
                    "message" : "Application Unsuccessful!"
                }

    else:

        return {
                
                "message" : "Something went wrong during the application process."
        }



        



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)



    

