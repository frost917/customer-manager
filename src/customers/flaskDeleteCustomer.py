from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Response, g, Blueprint
from postgres.databaseConnection import PostgresControll

manager = Blueprint("deleteCustomer", __name__)

@manager.route("/customers/<customerID>", methods=['DELETE'])
@tokenVerify
@dataParsing
def deleteCustomer():
    customerData = dict()
    customerData["UUID"] = g.get("UUID")
    customerData["customerID"] = g.get("customerID")
    customerData["customerName"] = g.get("customerName")
    customerData["phoneNumber"] = g.get("phoneNumber")

    database = PostgresControll()
    queryResult = database.deleteCustomerData(customerData=customerData)

    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        result =  Response(databaseIsGone(), status=500)

    customerData["queryDate"] = datetime.now()

    import json
    result = Response(json.dumps(result), status=200)

    return result
