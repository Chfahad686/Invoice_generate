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
collection_invoice_module = 'Invoice_Module'
######################################


invoice_mod= Blueprint('invoice_mod', __name__)

@invoice_mod.route('/create_invoice', methods=['POST'])
def create_invoice_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('DateOfService', required=True)
    parser.add_argument('NameOfCompany', required=True)
    parser.add_argument('ServiceId', required=True)
    parser.add_argument('NameOfCustomer', required=True)
    parser.add_argument('CustomerId', required=True) 
    
        # parse arguments to dictionary
    args = parser.parse_args()


    InvoiceID = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    print(InvoiceID)

    result_find=db[collection_invoice_module].find_one({"InvoiceID": InvoiceID})
    
    if result_find:
        return {
            'message id: email': f"'{InvoiceID}'' already exists" 
            }, 409


    db[collection_invoice_module].insert_one(
        {"InvoiceID": InvoiceID, "DateOfService": args["DateOfService"] , "NameOfCompany": args["NameOfCompany"], "ServiceId": args["ServiceId"] , "NameOfCustomer": args["NameOfCustomer"], "CustomerId": args["CustomerId"]}
        )
        #Read Operation
    Invoiceget=db[collection_invoice_module].find({"InvoiceID": InvoiceID})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Invoiceget]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
    ###################################################################################################

@invoice_mod.route('/update_invoice', methods=['PUT'])
def update_invoice_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('InvoiceID', required=True)
    parser.add_argument('DateOfService', required=True)
    parser.add_argument('NameOfCompany', required=True)
    parser.add_argument('ServiceId', required=True)
    parser.add_argument('NameOfCustomer', required=True)
    parser.add_argument('CustomerId', required=True)     
        # parse arguments to dictionary
    args = parser.parse_args()

    db[collection_invoice_module].update_one(
         {"InvoiceID":args["InvoiceID"]},
         {
             "$set":{
                 "DateOfService":args["DateOfService"],
                 "NameOfCompany":args["NameOfCompany"],
                 "ServiceId":args["ServiceId"],
                 "NameOfCustomer":args["NameOfCustomer"],
                 "CustomerId":args["CustomerId"]
                 }
         })
         
    Invoiceget1=db[collection_invoice_module].find({"InvoiceID": args["InvoiceID"]})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Invoiceget1]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
    ###################################################################################################

@invoice_mod.route('/delete_invoice', methods=['DELETE'])
def delete_invoice_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('InvoiceID', required=True)
    args = parser.parse_args()  # parse arguments to dictionary
        
    db[collection_invoice_module].delete_many(
        {
            "InvoiceID":args["InvoiceID"]
        })
        
    return {
        'message': f"'{args['InvoiceID']}' is deleted."
        }


    ###################################################################################################

@invoice_mod.route('/get_invoice', methods=['GET'])
def get_invoice_data():

    parser = reqparse.RequestParser()  # initialize    
    parser.add_argument('InvoiceID', required=True)
    args = parser.parse_args()  # parse arguments to dictionary

    Invoiceget2=db[collection_invoice_module].find({"InvoiceID": args["InvoiceID"]})
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Invoiceget2]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code



    ###################################################################################################

@invoice_mod.route('/get_all_Invoice', methods=['GET'])
def get_all_invoice_data():

    Invoiceget3=db[collection_invoice_module].find()
    
    #iterate over to get a list of dicts
    details_dicts = [doc for doc in Invoiceget3]
    #serialize to json string
    details_json_string = json.dumps(details_dicts,default=json_util.default)
    json_docs= json.loads(details_json_string)
    return {'data': json_docs}, 200  # return data and 200 OK code
