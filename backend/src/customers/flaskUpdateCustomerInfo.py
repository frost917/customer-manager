from dataCheck import customerDataCheck
from json import dumps

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint("updateCustomerData", __name__, url_prefix='/customers')

@manager.route('', methods=['PUT'])
@tokenVerify
@dataParsing
@customerDataCheck
def updateCustomerData():
    customers = g.get('customers')
    database = PostgresControll()
    payload = dict()

    for customer in customers:
        customerData = dict()
        customerID = customer.get('customerID')
        customerName = customer.get('customerName')
        phoneNumber = customer.get('phoneNumber')

        customerData['customerID'] = customerID
        customerData['customerName'] = customerName
        customerData['phoneNumber'] = phoneNumber

        queryResult = database.updateCustomerData(customerData=customerData)

        if queryResult is False:
            from msg.jsonMsg import databaseIsGone
            result = Response(databaseIsGone(), status=500,content_type="application/json; charset=UTF-8")
        else:
            payload[customerID] = customerData

    result = Response(dumps(payload), status=200, content_type="application/json; charset=UTF-8")

    return result
