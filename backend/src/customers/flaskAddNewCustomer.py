from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from msg.jsonMsg import databaseIsGone
from postgres.databaseConnection import PostgresControll

manager = Blueprint("addNewCustomer", __name__, url_prefix='/customers')

@manager.route("", methods=['POST'])
@tokenVerify
@dataParsing
def addNewCustomer():
    UUID = g.get('UUID')
    temp = list()

    import uuid
    database = PostgresControll()
    customers = g.get('customers')
    for data in customers:
        customerData = dict()
        customerData['customerID'] = str(uuid.uuid4())
        customerData['customerName'] = data.get('customerName')
        customerData['phoneNumber'] = data.get('phoneNumber')

        # 시술에 실패한 경우 DB가 죽은 것
        if database.addNewCustomer(UUID = UUID, customerData=customerData) is True:
            temp.append(customerData)
        else:
            return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    tasks = { "customerData": temp}

    from json import dumps
    return Response(dumps(tasks), status=200, content_type="application/json; charset=UTF-8")
