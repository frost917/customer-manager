﻿from datetime import datetime
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

    result = database.addNewCustomer(userData=convDict)
    if result is True:
        from json import dumps
        convList['successed'] = convList

        return Response(dumps(convList), status=200, mimetype="application/json")

    else:
        return Response(status=500)