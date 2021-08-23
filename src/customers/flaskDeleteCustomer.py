from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Response, g, request
from main import app
from postgres.databaseConnection import PostgresControll


@app.route("/customers/<customerID>", method=['DELETE'])
@tokenVerify
@dataParsing
def getCustomerData():

    customerData = dict()
    customerData["UUID"] = g.get("UUID")
    customerData["customerID"] = g.get("customerID")
    customerData["name"] = g.get("name")
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
