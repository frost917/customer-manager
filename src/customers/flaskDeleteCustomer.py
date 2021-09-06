from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('deleteCustomer', __name__, url_prefix='/customers')

@manager.route('/<customerID>', methods=['DELETE'])
@tokenVerify
def deleteCustomer(customerID):
    UUID = g.get('UUID')
    database = PostgresControll()

    result = database.deleteCustomerData(customerID=customerID)

    from json import dumps
    if result == True:
        return Response(dumps({'UUID': UUID, 'customerID': customerID, 'status': 'successed'}), status=200, mimetype="application/json")
    else:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype="application/json")
    
