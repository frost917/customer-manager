from json import dumps

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint("getCustomerList", __name__, url_prefix='/customers')

@manager.route("", methods=['GET'])
@tokenVerify
@dataParsing
def getCustomerList():
    UUID = g.get('UUID')

    # UUID를 이용해 고객 명단 불러옴
    database = PostgresControll()
    customerDict = database.getCustomerDict(UUID=UUID)

    # DB 에러인 경우에만 None 반환하므로
    # None인 경우 DB에러로 간주
    if customerDict is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500,mimetype="application/json")

    customers = list()

    # 고객 정보 패키징
    for customer in customerDict:
        customerData = dict()
        temp = dict()
        
        temp['customerName'] = customer.get('customer_name')
        temp['phoneNumber'] = customer.get('phone_number')
        customerData[customer.get('customer_id')] = temp

        customers.append(customerData)

    return Response(dumps({'UUID': UUID, 'customers': customers}), status=200, mimetype="application/json")