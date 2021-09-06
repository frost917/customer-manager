from datetime import datetime
from json import dumps

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint("addNewCustomer", __name__, url_prefix='/customers')

@manager.route("", methods=['POST'])
@tokenVerify
@dataParsing
def addNewCustomer():
    successedList = list()
    failedList = list()

    UUID = g["UUID"]

    import uuid
    database = PostgresControll()
    for data in g.customers:
        customerData = dict()
        customerData['customerName'] = data.get('customerName')
        customerData['phoneNumber'] = data.get('phoneNumber')
        customerData['customerID'] = uuid.uuid4()

        if database.addNewCustomer(UUID = UUID, customerData=customerData) is True:
            successedList.append(customerData)
        else:
            failedList.append(customerData)

    tasks = dict()

    tasks['UUID'] = UUID
    tasks['addDate'] = datetime.now()
    if successedList.count() != 0:
        tasks['successed'] = successedList
    if failedList.count() != 0:
        tasks['failed'] = failedList

    return Response(dumps(tasks), status=200)
