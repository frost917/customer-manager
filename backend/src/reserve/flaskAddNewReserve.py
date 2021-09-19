import json
import uuid
from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('addNewReserve', __name__, url_prefix='/reserves')

# 손님 한 명의 예약 추가
@manager.route('/customer/<customerID>', methods=['POST'])
@tokenVerify
@dataParsing
def addNewReserve(customerID):
    # 받아오는 데이터: 손님 id, 예약 시간, 시술 타입
    # 생성 후 반환하는 데이터: 손님 id, 예약 id, 시술 타입, 예약 시간
    reserve = g.get('reserves')[0]
    database = PostgresControll()

    print(reserve)

    print('손님 데이터 확인')
    isCustomer = database.getCustomerData(customerID=customerID)
    if len(isCustomer) == 0:
        from msg.jsonMsg import customerNotFound
        return Response(customerNotFound(), status=404, content_type='application/json; charset=UTF-8') 

    print('예약 데이터 패키징')
    # 예약 데이터 패키징
    reserveData = dict()
    reserveData['customerID'] = customerID
    reserveData['reserveID'] = str(uuid.uuid4())
    reserveData['reserveTime'] = reserve.get('reserveTime')
    reserveData['reserveType'] = reserve.get('reserveType')

    print(reserveData)
    print('예약 데이터 추가')
    result = database.addNewReserve(g.get('UUID'), reserveData=reserveData)

    if result is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    print('예약 데이터 추가 완료')
    returnData = {'reserveData': [ reserveData ]}

    return Response(json.dumps(returnData), status=200, content_type="application/json; charset=UTF-8")
