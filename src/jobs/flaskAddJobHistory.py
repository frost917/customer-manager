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

    returnData = dict()
    returnData['jobID'] = jobData   
    returnData[jobID]['customerID'] = g['customerID']
    returnData[jobID]['jobPrice'] = jobData['jobPrice']
    returnData[jobID]['jobDate'] = str(datetime.now())
    returnData[jobID]['jobDescribe'] = jobData['jobDescribe']

    return Response(json.dumps(returnData), status=200, mimetype='application/json')