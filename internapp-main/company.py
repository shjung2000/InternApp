from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from os import environ
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/company'
#app.config['SQLALCHEMY_DATABASE_URI'] =  environ.get('dbURL') or 'mysql+mysqlconnector://root:root@localhost:8889/company'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app) 
class Company(db.Model):
    __tablename__ = 'company'

    companyID = db.Column(db.Integer, primary_key = True)
    companyEmail = db.Column(db.String(100), nullable=False)
    companyName = db.Column (db.String(100), nullable=False)
    companyDesc = db.Column(db.String(100), nullable=False)
    companySize = db.Column(db.Integer)
    companyPassword = db.Column(db.String(100), nullable=False)

    def __init__(self, companyID, companyEmail, companyName, companyDesc, companySize, companyPassword):
        self.companyID = companyID
        self.companyEmail = companyEmail
        self.companyName = companyName
        self.companyDesc = companyDesc
        self.companySize = companySize
        self.companyPassword = companyPassword

    def json(self):
        return {
            "companyID": self.companyID,
            "companyEmail": self.companyEmail,
            "companyName": self.companyName,
            "companyDesc": self.companyDesc,
            "companySize": self.companySize,
            "companyPassword": self.companyPassword
        }

@app.route("/company")
def get_all():
    companylist = Company.query.all()
    if len(companylist):
        return jsonify({
            "code": 200,
            "data":{
                "companies": [company.json() for company in companylist]
            }
        })
    return jsonify({
        "code": 404,
        "message": "There are no companies"
    }), 404

# create new posting
@app.route("/company/<int:companyID>", methods=['POST'])
def create_company(companyID):
    if (Company.query.filter_by(companyID=companyID).first()):
        return jsonify({
            "code": 400,
            "data": {
                "companyID": companyID
            },
            "message": "Company already exists."
        }), 400
    
    data = request.get_json()
    company = Company(companyID, **data)

    try:
        db.session.add(company)
        db.session.commit()
    except:
        return jsonify({
            "code": 500,
            "data": {
                "companyID": companyID
            },
            "message": "An error occurred creating the company's profile"
        }), 500

    return jsonify(
        {
            "code": 201,
            "data": company.json()
        }
    ), 201


#for complex microservice cross checking
@app.route("/company_check")
def company_check():
    companyID = request.json.get("companyID" , None)

    company = Company.query.filter_by(companyID = companyID).first()
    if company:
        newId = random.randint(1, 10000)
        return jsonify(
            {
                "code": 200,
                "data": company.json(),
                "newId": newId,
                "message": "New jobID for the creation of new job posting has been created!"
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "The company does not exist."
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
    