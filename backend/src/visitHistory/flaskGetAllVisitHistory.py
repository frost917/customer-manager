from datetime import datetime
from json import dumps

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Flask, Response, g, request

manager = Blueprint("getAllVisitHistory", __name__, url_prefix='/visit-history')

@manager.route('/', methods=['GET'])
@tokenVerify
@dataParsing
def getAllVisitHistory():
    from postgres.databaseConnection import PostgresControll
    database = PostgresControll()

    result = database.getVisitHistoryDict(UUID=g['UUID'])

    if result is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype='application/json')

    else:
        payload = dict()
        convList = list()
        payload['UUID'] = g['UUID']
        payload['queryDate'] = datetime.now()
        convList.append(result)
        payload['data'] = convList
        return Response(dumps(payload), status=200, mimetype='application/json')
