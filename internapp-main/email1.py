from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#if mac
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/bookings'
#if windows
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bookings'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# db = SQLAlchemy(app)
CORS(app)

@app.route("/send", methods=['POST'])
def send_email():
    payload = json.loads(request.data)
    mail_content = Mail(
    from_email='estherrrlychee@gmail.com',
    to_emails=payload["to_emails"],
    subject=payload["subject"],
    html_content=("Dear user, Thank you for contacting Pudding. We are in the midst of processing your application.Thank you for your kind understanding." if payload["message"] == '' else payload["message"]))

    try:
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient("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")
        response = sg.send(mail_content)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return jsonify(
            {
                "code": 200,
                "message": "Email Sent!"
            }
        ), 200
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 502,
                "message": e
            }
        ), 502

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5007, debug = True)