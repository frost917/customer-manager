from main import app
from flask import Response, g, request
from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

@app.route("/customers/<customerID>", method=['PUT'])
@tokenVerify
@dataParsing
def updateCustomerInfo():
    import postgres.databaseConnection
    database = postgres.databaseConnection.PostgresControll()

    name = g["name"]
    phoneNumber = g["phoneNumber"]
    customerID = g["customerID"]
    UUID = g["UUID"]

    customerData = dict()
    customerData["customerID"] = customerID
    customerData["name"] = name
    customerData["phoneNumber"] = phoneNumber

    result = database.getCustomerInfo(UUID=UUID, customerID=customerID)

    import json
    return Response(json.dumps(result), status=200)
