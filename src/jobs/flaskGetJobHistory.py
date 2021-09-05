import json

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('getJobHistory', __name__, url_prefix='/jobs')

# 특정 작업 id의 데이터를 불러옴
@manager.route('/<customerID>/<jobID>', methods=['GET'])
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
