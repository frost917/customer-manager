from datetime import datetime
from main import app
from flask import Response, g, request
from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

@app.route("/customers/<customerID>", method=['GET'])
@tokenVerify
@dataParsing
def getCustomerData():
    UUID = g["UUID"]
    customerID = g["customerID"]

    userData = dict()
    userData["UUID"] = UUID
    userData["customerID"] = customerID

    import postgres.databaseConnection
    database = postgres.databaseConnection.PostgresControll()

    queryResult = database.getCustomerData(userData=userData)

    if queryResult is None:
        from msg.jsonMsg import databaseIsGone
        result =  Response(databaseIsGone(), status=500)

    customerData = dict()   
    customerData["name"] = queryResult.get("name")
    customerData["phoneNumber"] = queryResult.get("phone_number")
    customerData["queryDate"] = datetime.now()

    import json
    result = Response(json.dumps(result), status=200)

    return result