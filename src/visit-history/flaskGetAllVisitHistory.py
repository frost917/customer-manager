from flask import Flask, Blueprint, request, g, Response
from dataProcess import dataParsing
from auth.flaskAuthVerify import tokenVerify
from json import dumps 
from datetime import datetime
manager = Blueprint("getAllVisitHistory", __name__)

@manager.route('/visit-history', methods=['GET'])
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
        payload['UUID'] = g['UUID']
        payload['queryDate'] = datetime.now()
        payload['data'] = result
        return Response(dumps(payload), status=200, mimetype='application/json')