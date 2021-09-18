import json
import uuid
from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('addJobHistory', __name__, url_prefix='/reserve')

# 단일 손님에 대한 단일 데이터만 책임짐
@manager.route('/<customerID>', methods=['POST'])
@tokenVerify
@dataParsing
def addNewReserve(customerID):
    # 받아오는 데이터: 손님 id, 예약 시간, 시술 타입
    # 생성 후 반환하는 데이터: 손님 id, 예약 id, 시술 타입, 예약 시간
    reserve = g.get('reserveData')[0]
    database = PostgresControll()
    convList = list()

    isCustomer = database.getCustomerData(customerID=customerID)
    if len(isCustomer) == 0:
        from msg.jsonMsg import customerNotFound
        return Response(customerNotFound(), status=404, content_type='application/json; charset=UTF-8') 

    # 예약 데이터 패키징
    reserveData = dict()
    reserveData['customerID'] = customerID
    reserveData['reserveID'] = str(uuid.uuid4())
    reserveData['reserveTime'] = reserve.get('reserveTime')
    reserveData['reserveType'] = reserve.get('reserveType')

    result = database.addNewReserve(g.get('UUID'), reserveData=reserveData)

    if result is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    convList.append(reserveData)

    returnData = dict()
    returnData['reserveData'] = convList

    return Response(json.dumps(returnData), status=200, content_type="application/json; charset=UTF-8")
