from main import app
from flask import Response, g, request
from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from json import dumps

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

    queryResult = database.getCustomerInfo(UUID=UUID, customerID=customerID)

    if queryResult is None:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")
    else:
        result = Response(dumps(queryResult), status=200, mimetype="application/json")

    return result