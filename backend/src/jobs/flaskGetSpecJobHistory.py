import json

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('getSpecJobHistory', __name__, url_prefix='/jobs')

# 특정 고객의 모든 작업 기록을 불러옴
@manager.route('/<customerID>', methods=['GET'])
@tokenVerify
@dataParsing
def getJobHistory(jobID):
    database = PostgresControll()

    result = database.getJobsHistory(jobID=jobID)
    if result is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype='application/json',content_type='application/json')

    convList = list()
    payload = dict()

    convList.append(result)
    payload[jobID] = convList

    return Response(json.dumps(payload), status=200, mimetype='application/json', content_type='application/json')
