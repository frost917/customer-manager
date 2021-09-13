from dataCheck import customerDataCheck
from json import dumps

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint("updateCustomerData", __name__, url_prefix='/customers')

@manager.route("/<customerID>", methods=['PUT'])
@tokenVerify
@dataParsing
@customerDataCheck
def updateCustomerData(customerID):
    customers = g.get('customers')
    data = customers.index(0)

    customerData = dict()
    customerData['customerID'] = customerID
    customerData['customerName'] = data.get('customerName')
    customerData['phoneNumber'] = data.get('phoneNumber')

    database = PostgresControll()
    queryResult = database.updateCustomerData(customerData=customerData)

    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")
    else:
        temp = dict()
        temp['customerName'] = data.get('customerName')
        temp['phoneNumber'] = data.get('phoneNumber')

        payload = dict()
        payload[customerID] = temp

        result = Response(dumps(payload), status=200, mimetype="application/json")

    return result
