from flask import Blueprint
import json
import pymongo
#from datetime import timedelta
import redis
#from pymongo import MongoClient
from flask import Flask, jsonify, request
#from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token,get_jwt
import pandas as pd
#import ast
from bson import json_util
import hashlib
#import jwt
import random
import string
from database import db
#####################################
collection_admin_signup = 'Login_Module'
######################################

login= Blueprint('login', __name__)

@login.route('/admin_signup', methods=['POST'])
def admin_signup_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('Email', required=True)
    parser.add_argument('Password', required=True) 
    
        # parse arguments to dictionary
    args = parser.parse_args()



    #############################hashing password
    
    t_password=args["Password"]
    t_hashed = hashlib.sha3_512(t_password.encode())
    t_password = t_hashed.hexdigest()
    args["Password"] = t_password
    ################################
    
    AdminID = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    print(AdminID)

    result_find=db[collection_admin_signup].find_one({"Email":args["Email"]})
    
    if result_find:
        return {
            'message id: email': f"'{args['Email']}'' already exists" 
            }, 409

    db[collection_admin_signup].insert_one(
        {"AdminID": AdminID, "Email": args["Email"] , "Password": args["Password"]}
        )
        #Read Operation
    Adminget=db[collection_admin_signup].find({"AdminID": AdminID})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Adminget]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
    ###################################################################################################


@login.route('/admin_login', methods=['POST'])
def admin_login_data():
    
    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('Email', required=True)
    parser.add_argument('Password', required=True) 
    
        # parse arguments to dictionary
    args = parser.parse_args()

###################################################################
                            #hashing password
    
    new_password=args["Password"]
    new_t_hashed = hashlib.sha3_512(new_password.encode())
    hashed_password = new_t_hashed.hexdigest()
############################################################################


    # Read operation
#    result=db[collection_admin_signup].find({"Email":args["Email"]})
    result_owner=db[collection_admin_signup].find({"Email":args["Email"],"Password":hashed_password})
    
    jsn_docs = []
    jsn_result = ''
    for i in result_owner:
        jsn_result = json.dumps(i, default=json_util.default)
        jsn_docs.append(jsn_result)

    if jsn_result:
        return {'Message': 'Login Succeeded', 'data': json.loads(jsn_result)}, 200
    else:
         return {'Message': 'Login Failed Wrong Email or Wrong Password',}, 400

###############################################################################################################

# @login.route('/Change_Password', methods=['PUT'])
# def admin_change_password():

#     parser = reqparse.RequestParser()  # initialize    
#     parser.add_argument('Email', required=True)
#     parser.add_argument('Password', required=True) 
#         # parse arguments to dictionary
#     args = parser.parse_args()

# ###################################################################
#                             #hashing password
    
#     new_password=args["Password"]
#     new_t_hashed = hashlib.sha3_512(new_password.encode())
#     hashed_password = new_t_hashed.hexdigest()
# ############################################################################

    # db[collection_admin_signup].update_one(
    #     {"DiagnoseID":args["DiagnoseID"]},
    #     {
    #         "$set":{
    #             "IssueStatus":"COMPLETED"
    #             }
    #     })


    #         #Read Operation
    # diagnose_get2=db[collection_admin_signup].find({"DiagnoseID":args["DiagnoseID"]})
    
    # #iterate over to get a list of dicts
    # details_dicts = [doc for doc in diagnose_get2]
    # #serialize to json string
    # details_json_string = json.dumps(details_dicts,default=json_util.default)
    # json_docs= json.loads(details_json_string)
    # return {'data': json_docs}, 200  # return data and 200 OK code