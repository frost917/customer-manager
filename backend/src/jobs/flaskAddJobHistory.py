from backend.src.dataCheck import customerDataCheck
import json
import uuid
from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('addJobHistory', __name__, url_prefix='/jobs')

@manager.route('/<customerID>/jobs', methods=['POST'])
@customerDataCheck
def addJobHistory(customerID):
    # 받아오는 데이터: 손님 id, 작업 비용, 작업 기록, 작업 목록
    # 생성 후 반환하는 데이터: 작업 id, 방문 날짜, 작업 id

    jobData = dict(g['jobData'])
    jobData['jobID'] = str(uuid.uuid4())
    jobData['customerID'] = g['customerID']
    jobData['visitDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    jobData['jobFinished'] = g['jobFinished']
    jobData['jobPrice'] = g['jobPrice']
    jobData['jobDescription'] = g['jobDescription']

    database = PostgresControll()
    result = database.addNewJob(jobData=g['jobData'])

    if result is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype='application/json')

    temp = dict()
    temp['customerID'] = g['customerID']
    temp['jobPrice'] = jobData['jobPrice']
    temp['jobDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp['jobDescription'] = jobData['jobDescription']

    convList = list()
    convList.append(temp)

    jobID = jobData['jobID']
    returnData = dict()
    returnData[jobID] = convList

    return Response(json.dumps(temp), status=200, mimetype='application/json')
