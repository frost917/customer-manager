import json

from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify

manager = Blueprint('getAllJobHistory', __name__, url_prefix='/jobs')

@manager.route('', methods=['GET'])
@tokenVerify
def getAllJobHistory():
    database = PostgresControll()

    UUID = g.get('UUID')
    reserves = database.getAllReserve(UUID=UUID)

    if reserves is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    elif len(reserves) == 0:
        from msg.jsonMsg import jobNotFound
        return Response(jobNotFound(), status=404, content_type="application/json; charset=UTF-8")

    convList = list()

    # 전체 데이터 패키징
    for reserve in reserves:
        temp = dict()
        reserveID = reserve.get('reserve_id')
        reserveData = database.getReserveData(reserveID=reserveID)
        reserveTypes = database.getReserveType(reserveID=reserveID)

        customerID = reserveData.get('customer_id')
        # 시간 쿼리했을 경우 datetime 객체로 불러와짐
        reserveTime = reserveData.get('reserve_time').strftime('%Y-%m-%d %H:%M')

        # 단일 데이터 패키징
        temp['customerID'] = customerID
        temp['reserveID'] = reserveID

        # 시술 타입 패키징
        types = list()
        for reserveType in reserveTypes:
            types.append(reserveType)
        temp['reserveType'] = types

        temp['reserveTime'] = reserveTime
        convList.append(temp)

    payload = dict()
    payload['reserveData'] = convList

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")
