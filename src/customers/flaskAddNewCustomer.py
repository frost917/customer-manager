from datetime import datetime
from main import app
from flask import Flask, g, request, Response
from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

@app.route("/customers", method=['POST'])
@tokenVerify
@dataParsing
def addNewCustomer():
    convDict = dict()
    convList = list()

    UUID = g["UUID"]
    name = g["name"]
    phoneNumber = g["phoneNumber"]
    import uuid
    customerID = uuid.uuid4()

    import postgres.databaseConnection
    database = postgres.databaseConnection.PostgresControll()

    convDict['UUID'] = UUID
    convDict['name'] = name
    convDict['phoneNumber'] = phoneNumber
    convDict['customerID'] = customerID
    convDict['addDate'] = datetime.now()

    queryResult = database.addNewCustomer(userData=convDict)
    if queryResult is True:
        from json import dumps
        convList['successed'] = queryResult

        result = Response(dumps(convList), status=200, mimetype="application/json")

    else:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")

    return result