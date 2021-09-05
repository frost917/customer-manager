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
    UUID = g['UUID']

    userData = dict()
    userData['UUID'] = UUID
    userData['customerID'] = customerID

    queryResult = PostgresControll().getCustomerData(userData=userData)

    if queryResult is None:
        from msg.jsonMsg import databaseIsGone
        result =  Response(databaseIsGone(), status=500)

    customerData = dict()   
    customerData['customerName'] = queryResult.get('customerName')
    customerData['phoneNumber'] = queryResult.get('phoneNumber')
    customerData['queryDate'] = datetime.now()

    import json
    result = Response(json.dumps(result), status=200)

    return result
