﻿from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Response, g, Blueprint
from postgres.databaseConnection import PostgresControll

manager = Blueprint("getCustomerData", __name__)

@manager.route("/customers/<customerID>", methods=['GET'])
@tokenVerify
@dataParsing
def getCustomerData():
    UUID = g["UUID"]
    customerID = g["customerID"]

    userData = dict()
    userData["UUID"] = UUID
    userData["customerID"] = customerID

    queryResult = PostgresControll().getCustomerData(userData=userData)

    if queryResult is None:
        from msg.jsonMsg import databaseIsGone
        result =  Response(databaseIsGone(), status=500)

    customerData = dict()   
    customerData["customerName"] = queryResult.get("customerName")
    customerData["phoneNumber"] = queryResult.get("phoneNumber")
    customerData["queryDate"] = datetime.now()

    import json
    result = Response(json.dumps(result), status=200)

    return result
