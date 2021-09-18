import json

from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify

manager = Blueprint('updateReserveData', __name__, url_prefix='/reserves')

@manager.route('', methods=['PUT'])
@tokenVerify
def updateReserveData():
    database = PostgresControll()

    reserveData = g.get('reserveData')

    result = database.updateReserveData(reserveData=reserveData)

    if result is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    return Response(json.dumps('Successed'), status=200, content_type="application/json; charset=UTF-8")
