from main import app
from flask import Response, g
from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from json import dumps
from postgres.databaseConnection import PostgresControll

@app.route("/customers/<customerID>", method=['PUT'])
@tokenVerify
@dataParsing
def updateCustomerData():
    name = g["name"]
    phoneNumber = g["phoneNumber"]
    customerID = g["customerID"]

    customerData = dict()
    customerData["customerID"] = customerID
    customerData["name"] = name
    customerData["phoneNumber"] = phoneNumber

    database = PostgresControll()
    queryResult = database.updateCustomerData(customerData=customerData)

    if queryResult is False:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")
    else:
        result = Response(dumps(customerData), status=200, mimetype="application/json")

    return result