from datetime import datetime

from dataProcess import dataParsing
from flask import Response, g, Blueprint
from postgres.databaseConnection import PostgresControll

manager = Blueprint('getCustomerData', __name__, url_prefix='/customers')

@manager.route('/<customerID>', methods=['GET'])
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
