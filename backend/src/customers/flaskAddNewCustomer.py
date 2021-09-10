from datetime import datetime

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

        # 작업에 성공한 경우와 실패한 경우를 따로 나누어 json으로 반환
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

    from json import dumps
    return Response(dumps(tasks), status=200, mimetype="application/json")