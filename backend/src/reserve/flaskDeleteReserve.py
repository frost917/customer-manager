import json

from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify

manager = Blueprint('deleteReserveData', __name__, url_prefix='/reserves')

# 해당 id로 된 예약 삭제
@manager.route('/<reserveID>', methods=['DELETE'])
@tokenVerify
def deleteReserveData(reserveID):
    database = PostgresControll()
    result = database.deleteReserveData(reserveID=reserveID)

    if result is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    return Response(json.dumps('Successed'), status=200, content_type="application/json; charset=UTF-8")
