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
collection_service_module = 'Service_Module'
######################################


service_mod= Blueprint('service_mod', __name__)

@service_mod.route('/create_service', methods=['POST'])
def create_service_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('ServiceName', required=True)
    parser.add_argument('ServiceDesc', required=True)
    parser.add_argument('HoursWorked', required=True)
    parser.add_argument('RatePerHour', required=True)
#    parser.add_argument('Email', required=True) 
    
        # parse arguments to dictionary
    args = parser.parse_args()


    ServiceID = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    print(ServiceID)

    result_find=db[collection_service_module].find_one({"ServiceID": ServiceID})
    
    if result_find:
        return {
            'message id: email': f"'{ServiceID}'' already exists" 
            }, 409

    db[collection_service_module].insert_one(
        {"ServiceID": ServiceID, "ServiceName": args["ServiceName"] , "ServiceDesc": args["ServiceDesc"], "HoursWorked": args["HoursWorked"] , "RatePerHour": args["RatePerHour"]}
        )
        #Read Operation
    Serviceget=db[collection_service_module].find({"ServiceID": ServiceID})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Serviceget]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
    ###################################################################################################

@service_mod.route('/update_service', methods=['PUT'])
def update_service_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('ServiceID', required=True)
    parser.add_argument('ServiceName', required=True)
    parser.add_argument('ServiceDesc', required=True)
    parser.add_argument('HoursWorked', required=True)
    parser.add_argument('RatePerHour', required=True)
#    parser.add_argument('Email', required=True) 
    
        # parse arguments to dictionary
    args = parser.parse_args()

    db[collection_service_module].update_one(
         {"ServiceID":args["ServiceID"]},
         {
             "$set":{
                 "ServiceName":args["ServiceName"],
                 "ServiceDesc":args["ServiceDesc"],
                 "HoursWorked":args["HoursWorked"],
                 "RatePerHour":args["RatePerHour"]
                 }
         })
         
    Serviceget1=db[collection_service_module].find({"ServiceID": args["ServiceID"]})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Serviceget1]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
    ###################################################################################################

@service_mod.route('/delete_service', methods=['DELETE'])
def delete_service_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('ServiceID', required=True)
    args = parser.parse_args()  # parse arguments to dictionary
        
    db[collection_service_module].delete_many(
        {
            "ServiceID":args["ServiceID"]
        })
        
    return {
        'message': f"'{args['ServiceID']}' is deleted."
        }


    ###################################################################################################

@service_mod.route('/get_service', methods=['GET'])
def get_service_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('ServiceID', required=True)
    args = parser.parse_args()  # parse arguments to dictionary

    Serviceget2=db[collection_service_module].find({"ServiceID": args["ServiceID"]})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Serviceget2]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code


    ###################################################################################################

@service_mod.route('/get_all_service', methods=['GET'])
def get_all_service_data():

    Serviceget3=db[collection_service_module].find()
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Serviceget3]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
