from datetime import datetime

from dataProcess import dataParsing
from flask import Response, g, Blueprint
from postgres.databaseConnection import PostgresControll

manager = Blueprint('deleteCustomer', __name__, url_prefix='/customers')

@manager.route('/<customerID>', methods=['DELETE'])
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
        result =  Response(databaseIsGone(), status=500)

    customerData['queryDate'] = datetime.now()

    import json
    result = Response(json.dumps(result), status=200)

    return result
