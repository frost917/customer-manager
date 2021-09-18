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
def addJobHistory(customerID):
    # 받아오는 데이터: 손님 id, 시술 비용, 시술 기록, 시술 목록
    # 생성 후 반환하는 데이터: 시술 id, 방문 날짜, 시술 id
    jobs = g.get('jobs')
    database = PostgresControll()
    convList = list()

    for job in jobs:
        jobData = dict()
        jobData['customerID'] = customerID
        jobData['jobID'] = str(uuid.uuid4())
        jobData['jobFinished'] = job.get('jobFinished')
        jobData['visitDate'] = datetime.now().strftime('%Y-%m-%d')
        jobData['jobPrice'] = job.get('jobPrice')
        jobData['jobDescription'] = job.get('jobDescription')
        result = database.addNewJob(jobData=jobData)

        if result is False:
            from msg.jsonMsg import databaseIsGone
            return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

        convList.append(jobData)

    returnData = dict()
    returnData['jobData'] = convList

    return Response(json.dumps(returnData), status=200, content_type="application/json; charset=UTF-8")
