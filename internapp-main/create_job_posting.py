from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ
import requests


from invokes import invoke_http



app = Flask(__name__)
CORS(app)

company_URL =  environ.get('company_URL') or "http://localhost:5002/company_check"
job_URL =  environ.get('job_URL') or "http://localhost:5003/job"



#When making a request, the request will be in JSON format and will look something like:
# {
# "companyID":2, //this needs to exist in the company database as well
# "jobName": "IT Helper",
# "postDate": "2022-04-02",
# "jobDesc": "something",
# "deadline": "2022-06-22"
# }

@app.route("/create_job", methods=['POST'])
def create_job():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            job_details = request.get_json()
            print("\nReceived job details in JSON:", job_details)

            result = processJobPosting(job_details) 
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_job_posting.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processJobPosting(job_details):

    check_company_exist = invoke_http(company_URL , method = 'GET' , json = job_details)
    print("\nCompany exists")

    company_check_code = check_company_exist["code"]
    print(check_company_exist)
    new_job_id = check_company_exist["newId"]
    
    if company_check_code == 200:
        
        jobCreate = invoke_http("".join((job_URL, "/", str(new_job_id))) , method = 'POST' , json = job_details)
        print(jobCreate)
        if jobCreate["code"] == 201:

            return {
                "code": 201,
                "message" : "Job Posting Successful!"
            }

        elif jobCreate["code"] == 400:

            return {
                "code": 400,
                "message" : "Failed to post job as the job is already existing"
            }

        elif jobCreate["code"] == 500:

            return {
                "code": 500,
                "message": "Opps.. something went wrong while creating job post"
            }
    else:

        return {
            "code": 404,
            "message" : "Company does not exist!"
        }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for creating job posting...")
    app.run(host="0.0.0.0", port=5200, debug=True)
