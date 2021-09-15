from dataCheck import customerDataCheck
import json
import uuid
from datetime import datetime

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('addJobHistory', __name__, url_prefix='/jobs')

# 단일 손님에 대한 단일 데이터만 책임짐
@manager.route('/<customerID>/job', methods=['POST'])
@tokenVerify
@dataParsing
@customerDataCheck
def addJobHistory(customerID):
    # 받아오는 데이터: 손님 id, 작업 비용, 작업 기록, 작업 목록
    # 생성 후 반환하는 데이터: 작업 id, 방문 날짜, 작업 id
    jobs = g.get('jobs')

    jobData = dict()
    jobData['customerID'] = customerID
    jobData['jobID'] = str(uuid.uuid4())
    jobData['jobFinished'] = jobs.get('jobFinished')
    jobData['visitDate'] = datetime.now().strftime('%Y-%m-%d')
    jobData['jobPrice'] = jobs.get('jobPrice')
    jobData['jobDescription'] = jobs.get('jobDescription')

    database = PostgresControll()
    result = database.addNewJob(jobData=jobData)

    if result is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    temp = dict()
    temp['jobFinished'] = jobData['jobFinished']
    temp['jobDate'] = jobData['visitDate']
    temp['jobPrice'] = jobData['jobPrice']
    temp['jobDescription'] = jobData['jobDescription']

    convList = list()
    convList.append(temp)

    jobID = jobData['jobID']
    returnData = dict()
    returnData[jobID] = convList

    return Response(json.dumps(temp), status=200, content_type="application/json; charset=UTF-8")
