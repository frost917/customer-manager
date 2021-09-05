from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint("addNewCustomer", __name__, url_prefix='/customers')

@manager.route("/", methods=['POST'])
@tokenVerify
@dataParsing
def addNewCustomer():
    customerData = dict()
    convList = list()

    UUID = g["UUID"]
    customerName = g["customerName"]
    phoneNumber = g["phoneNumber"]
    import uuid
    customerID = uuid.uuid4()

    customerData['UUID'] = UUID
    customerData['customerName'] = customerName
    customerData['phoneNumber'] = phoneNumber
    customerData['customerID'] = customerID
    customerData['addDate'] = datetime.now()

    database = PostgresControll()
    queryResult = database.addNewCustomer(userData=customerData)
    if queryResult is True:
        from json import dumps
        convList.append(queryResult)
        convDict = dict()
        convDict['successed'] = convList

        result = Response(dumps(convDict), status=200, mimetype="application/json")

    else:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")

    return result
