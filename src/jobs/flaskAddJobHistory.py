from _typeshed import ReadableBuffer
from datetime import datetime
from flask import Blueprint, g, Response
from dataProcess import dataParsing
import uuid
import json

from postgres.databaseConnection import PostgresControll

manager = Blueprint('addJobHistory', __name__, url_prefix='/jobs')

@manager.route('/', methods=['POST'])
@dataParsing
def addJobHistory():
    # 받아오는 데이터: 손님 id, 작업 비용, 작업 기록, 작업 목록
    # 생성 후 반환하는 데이터: 작업 id, 방문 날짜, 작업 id

    jobData = dict(g['jobData'])
    jobData['jobID'] = str(uuid.uuid4())
    jobData['customerID'] = g['customerID']

    database = PostgresControll()
    
    result = database.addNewJob(jobData=g['jobData'])

    if result is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype='application/json')

    jobID = jobData['jobID']

    temp = dict()
    temp['customerID'] = g['customerID']
    temp['jobPrice'] = jobData['jobPrice']
    temp['jobDate'] = str(datetime.now())
    temp['jobDescribe'] = jobData['jobDescribe']

    convList = list()
    convList.append(temp)

    returnData = dict()
    returnData[jobID] = convList

    return Response(json.dumps(temp), status=200, mimetype='application/json')