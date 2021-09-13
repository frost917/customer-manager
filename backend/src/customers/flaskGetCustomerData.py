from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('getCustomerData', __name__, url_prefix='/customers')

@manager.route('/<customerID>', methods=['GET'])
@tokenVerify
@dataParsing
def getCustomerData(customerID):
    database = PostgresControll()
    queryResult = database.getCustomerData(customerID=customerID)

    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        result =  Response(databaseIsGone(), status=500)

    customerData = dict()
    customerData['customerName'] = queryResult.get('customerName')
    customerData['phoneNumber'] = queryResult.get('phoneNumber')

    temp = dict()
    temp[customerID] = customerData

    from json import dumps
    result = Response(dumps(temp), status=200, mimetype="application/json")

    return result
