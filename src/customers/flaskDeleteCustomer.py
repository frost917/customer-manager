from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('deleteCustomer', __name__, url_prefix='/customers')

@manager.route('/<customerID>', methods=['DELETE'])
@tokenVerify
@dataParsing
def deleteCustomer(customerID):
    customerData = dict()
    customerData['UUID'] = g['UUID']
    customerData['customerID'] = customerID
    customerData['customerName'] = g['customerName']
    customerData['phoneNumber'] = g['phoneNumber']

    database = PostgresControll()
    queryResult = database.deleteCustomerData(customerData=customerData)

    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500)

    result = Response(status=200)

    return result
