import json
from flask import Blueprint, Response, g

from postgres.databaseConnection import PostgresControll
from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

manager = Blueprint('updateReserveData', __name__, url_prefix='/reserves')

@manager.route('', methods=['PUT'])
@tokenVerify
@dataParsing
def updateReserveData():
    database = PostgresControll()

    reserveData = g.get('reserves')

    for reserve in reserveData: 
        print(reserve)
        result = database.updateReserveData(reserveData=reserve)

        if result is False:
            from msg.jsonMsg import databaseIsGone
            return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    payload = dict()
    temp = list()
    temp.append(reserveData)
    payload['reserveData'] = temp

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")
