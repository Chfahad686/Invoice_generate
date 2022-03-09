from flask import Flask, render_template
from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
#from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt
from datetime import timedelta, datetime
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_mongo_sessions import MongoDBSessionInterface
###########################################################
from login_module.login import login
from service_module.service_mod import service_mod
from invoice_module.invoice_mod import invoice_mod
from customer_module.customer_mod import customer_mod
########################################
app = Flask(__name__)  
CORS(app)

app.secret_key = "mysecret" #secret key in session
app.permanent_session_lifetime = timedelta(minutes=1) #timeout of session

########################################

app.register_blueprint(login)
app.register_blueprint(service_mod)
app.register_blueprint(invoice_mod)
app.register_blueprint(customer_mod)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)  # run our Flask app