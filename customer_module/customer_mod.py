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
collection_customer_module = 'Customer_Module'
######################################


customer_mod= Blueprint('customer_mod', __name__)

@customer_mod.route('/create_cust_service', methods=['POST'])
def create_customer_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('CustomerName', required=True)
    parser.add_argument('DateOfWork', required=True)
    parser.add_argument('HoursWorked', required=True)
    parser.add_argument('RatePerHour', required=True)
#    parser.add_argument('Email', required=True) 
    
        # parse arguments to dictionary
    args = parser.parse_args()


    CustomerID = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    print(CustomerID)

    result_find=db[collection_customer_module].find_one({"CustomerID": CustomerID})
    
    if result_find:
        return {
            'message id: email': f"'{CustomerID}'' already exists" 
            }, 409

    db[collection_customer_module].insert_one(
        {"CustomerID": CustomerID, "CustomerName": args["CustomerName"] , "DateOfWork": args["DateOfWork"], "HoursWorked": args["HoursWorked"] , "RatePerHour": args["RatePerHour"]}
        )
        #Read Operation
    Customerget=db[collection_customer_module].find({"CustomerID": CustomerID})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Customerget]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
    ###################################################################################################

@customer_mod.route('/update_cust_service', methods=['PUT'])
def update_customer_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('CustomerID', required=True)
    parser.add_argument('CustomerName', required=True)
    parser.add_argument('DateOfWork', required=True)
    parser.add_argument('HoursWorked', required=True)
    parser.add_argument('RatePerHour', required=True)
#    parser.add_argument('Email', required=True) 
    
        # parse arguments to dictionary
    args = parser.parse_args()

    db[collection_customer_module].update_one(
         {"CustomerID":args["CustomerID"]},
         {
             "$set":{
                 "CustomerName":args["CustomerName"],
                 "DateOfWork":args["DateOfWork"],
                 "HoursWorked":args["HoursWorked"],
                 "RatePerHour":args["RatePerHour"]
                 }
         })
         
    Customerget1=db[collection_customer_module].find({"CustomerID": args["CustomerID"]})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Customerget1]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
    ###################################################################################################

@customer_mod.route('/delete_cust_service', methods=['DELETE'])
def delete_customer_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('CustomerID', required=True)
    args = parser.parse_args()  # parse arguments to dictionary
        
    db[collection_customer_module].delete_many(
        {
            "CustomerID":args["CustomerID"]
        })
        
    return {
        'message': f"'{args['CustomerID']}' is deleted."
        }


    ###################################################################################################

@customer_mod.route('/get_cust_service', methods=['GET'])
def get_service_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('CustomerID', required=True)
    args = parser.parse_args()  # parse arguments to dictionary

    Customerget2=db[collection_customer_module].find({"CustomerID": args["CustomerID"]})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Customerget2]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code


    ###################################################################################################

@customer_mod.route('/get_all_cust_service', methods=['GET'])
def get_all_service_data():

    Customerget3=db[collection_customer_module].find()
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Customerget3]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
