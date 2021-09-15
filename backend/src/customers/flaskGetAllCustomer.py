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
        return Response(databaseIsGone(), status=500,content_type="application/json; charset=UTF-8")

    customers = list()

    # 고객 정보 패키징
    for customer in customerDict:
        customerSpec = dict()
        temp = dict()
        
        temp['customerName'] = customer.get('customer_name')
        temp['phoneNumber'] = customer.get('phone_number')
        customerSpec[customer.get('customer_id')] = temp

        customers.append(customerSpec)

    customerData = dict()
    customerData['customerData'] = customers
    return Response(dumps(customerData), status=200, content_type="application/json; charset=UTF-8")