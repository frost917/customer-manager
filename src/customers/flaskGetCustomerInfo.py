from datetime import datetime
from main import app
from flask import Response, g, request
from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

@app.route("/customers/<customerID>", method=['GET'])
@tokenVerify
@dataParsing
def getCustomerInfo():
    UUID = g["UUID"]
    customerID = g["customerID"]

    userData = dict()
    userData["UUID"] = UUID
    userData["customerID"] = customerID

    import postgres.databaseConnection
    database = postgres.databaseConnection.PostgresControll()

    result = database.getCustomerInfo(userData=userData)

    if result is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500)

    customerInfo = dict()
    customerInfo["name"] = result[0]
    customerInfo["phoneNumber"] = result[1]
    customerInfo["queryDate"] = datetime.now()

    import json
    return Response(json.dumps(result), status=200)
