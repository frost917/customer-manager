from dataCheck import customerDataCheck
from json import dumps

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint("updateCustomerData", __name__, url_prefix='/customers')

@manager.route("", methods=['PUT'])
@tokenVerify
@dataParsing
@customerDataCheck
def updateCustomerData():
    customers = g.get('customers')
    database = PostgresControll()
    payload = dict()

    for id, data in customers.items():
        customerData = dict()
        customerID = id
        customerName = data.get('customerName')
        phoneNumber = data.get('phoneNumber')

        customerData['customerID'] = customerID
        customerData['customerName'] = customerName
        customerData['phoneNumber'] = phoneNumber

        queryResult = database.updateCustomerData(customerData=customerData)

        if queryResult is False:
            from msg.jsonMsg import databaseIsGone
            result = Response(databaseIsGone(), status=500,mimetype="application/json")
        else:
            temp = dict()
            temp['customerName'] = customerName
            temp['phoneNumber'] = phoneNumber

            payload[customerID] = temp

        result = Response(dumps(payload), status=200, mimetype="application/json")

    return result
