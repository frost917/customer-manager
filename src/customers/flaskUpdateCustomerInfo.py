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
    customers = list(g.get('customers'))
    data = dict(customers.index(0))

    customerData = dict()
    customerData['customerID'] = customerID
    customerData['customerName'] = data.get('customerName')
    customerData['phoneNumber'] = data.get('phoneNumber')

    database = PostgresControll()
    queryResult = database.updateCustomerData(customerData=customerData)

    # TODO 받아온 데이터가 없거나 해당 고객에 대한 데이터가 없을 경우에 대한 예외처리
    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")
    else:
        result = Response(dumps(customerData), status=200, mimetype="application/json")

    return result
