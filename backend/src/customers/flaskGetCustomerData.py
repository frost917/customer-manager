from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from dataCheck import customerDataCheck

from flask import Blueprint, Response
from postgres.databaseConnection import PostgresControll

manager = Blueprint('getCustomerData', __name__, url_prefix='/customers')

@manager.route('/<customerID>', methods=['GET'])
@tokenVerify
@dataParsing
@customerDataCheck
def getCustomerData(customerID):
    database = PostgresControll()
    queryResult = database.getCustomerData(customerID=customerID)

    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        result =  Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    customerData = dict()
    customerData['customerID'] = queryResult.get('customerID')
    customerData['customerName'] = queryResult.get('customerName')
    customerData['phoneNumber'] = queryResult.get('phoneNumber')

    temp = list()
    temp.append(customerData)

    from json import dumps
    result = Response(dumps(temp), status=200, content_type="application/json; charset=UTF-8")

    return result
