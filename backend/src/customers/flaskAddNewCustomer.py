from datetime import datetime

# from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll
from msg.jsonMsg import databaseIsGone

manager = Blueprint("addNewCustomer", __name__, url_prefix='/customers')

@manager.route("", methods=['POST'])
@dataParsing
def addNewCustomer():
    UUID = g.get('UUID')
    successedList = list()

    import uuid
    database = PostgresControll()
    customers = g.get('customers')
    for data in customers:
        customerData = dict()
        customerData['customerID'] = uuid.uuid4()
        customerData['customerName'] = data.get('customerName')
        customerData['phoneNumber'] = data.get('phoneNumber')

        # 작업에 실패한 경우 DB가 죽은 것
        if database.addNewCustomer(UUID = UUID, customerData=customerData) is True:
            successedList.append(customerData)
        else:
            return Response(databaseIsGone(), status=500, mimetype="application/json")

    tasks = dict()

    tasks['addDate'] = datetime.now()
    if len(successedList) != 0:
        tasks['successed'] = successedList

    from json import dumps
    return Response(dumps(tasks), status=200, mimetype="application/json")