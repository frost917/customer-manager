from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Response, g, Blueprint
from postgres.databaseConnection import PostgresControll

manager = Blueprint("addNewCustomer", __name__)

@manager.route("/customers", methods=['POST'])
@tokenVerify
@dataParsing
def addNewCustomer():
    convDict = dict()
    convList = list()

    UUID = g["UUID"]
    customerName = g["customerName"]
    phoneNumber = g["phoneNumber"]
    import uuid
    customerID = uuid.uuid4()

    convDict['UUID'] = UUID
    convDict['customerName'] = customerName
    convDict['phoneNumber'] = phoneNumber
    convDict['customerID'] = customerID
    convDict['addDate'] = datetime.now()

    database = PostgresControll()
    queryResult = database.addNewCustomer(userData=convDict)
    if queryResult is True:
        from json import dumps
        convList['successed'] = queryResult

        result = Response(dumps(convList), status=200, mimetype="application/json")

    else:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")

    return result
