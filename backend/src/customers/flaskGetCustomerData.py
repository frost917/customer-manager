from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from dataCheck import customerDataCheck

from flask import Blueprint, Response
from postgres.databaseConnection import PostgresControll

manager = Blueprint('getCustomerData', __name__, url_prefix='/customers')

@manager.route('/<customerID>', methods=['GET'])
@tokenVerify
def getCustomerData(customerID):
    database = PostgresControll()
    queryResult = database.getCustomerData(customerID=customerID)

    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        result =  Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    # TODO Dict가 아니라 리스트로 나오는 버그 있음
    customerData = dict()
    customerData['customerID'] = customerID
    customerData['customerName'] = queryResult[0]
    customerData['phoneNumber'] = queryResult[1]

    temp = list()
    temp.append(customerData)
    payload = dict()
    payload['customerData'] = temp

    from json import dumps
    result = Response(dumps(payload), status=200, content_type="application/json; charset=UTF-8")

    return result
