from dataCheck import customerDataCheck
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
@customerDataCheck
def getJobHistory(customerID):
    database = PostgresControll()

    jobData = database.getJobsSingleCustomer(customerID=customerID)

    if jobData is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    payload = dict()

    for job in jobData:
        temp = dict()

        temp['jobFinished'] = list()
        for jobType in job.get('job_finished'):
            temp['jobFinished'].append(jobType)

        temp['visitDate'] = job.get('visit_date')
        temp['jobPrice'] = int(job.get('job_price'))
        temp['jobDescription'] = job.get('job_description')

        jobID = job.get('job_id')
        payload[jobID] = temp

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")
