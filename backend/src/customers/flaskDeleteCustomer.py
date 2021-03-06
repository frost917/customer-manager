from dataCheck import customerDataCheck

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('deleteCustomer', __name__, url_prefix='/customers')

@manager.route('', methods=['DELETE'])
@tokenVerify
@dataParsing
@customerDataCheck
def deleteCustomer():
    customers = g.get('customers')
    database = PostgresControll()

    for customer in customers:
        customerID = customer.get('customerID')
        result = database.deleteCustomerData(customerID=customerID)

        from json import dumps
        if result == False:
            from msg.jsonMsg import databaseIsGone
            return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")
            
    # 전부 순회하면 반환
    return Response(dumps({'status': 'successed'}), status=200, content_type="application/json; charset=UTF-8")