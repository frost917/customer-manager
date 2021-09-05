from json import dumps

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint("updateCustomerData", __name__, url_prefix='/customers')

@manager.route("/<customerID>", methods=['PUT'])
@tokenVerify
@dataParsing
def updateCustomerData(customerID):

    customerData = dict()
    customerData["customerID"] = customerID
    customerData["customerName"] = g["customerName"]
    customerData["phoneNumber"] = g["phoneNumber"]

    database = PostgresControll()
    queryResult = database.updateCustomerData(customerData=customerData)

    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")
    else:
        result = Response(dumps(customerData), status=200, mimetype="application/json")

    return result
