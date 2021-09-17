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
@customerDataCheck
def getJobHistory(customerID):
    database = PostgresControll()
    jobData = database.getJobsSingleCustomer(customerID=customerID)

    if jobData is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    elif len(jobData) == 0:
        from msg.jsonMsg import jobNotFound
        return Response(jobNotFound(), status=404, content_type="application/json; charset=UTF-8")

    payload = dict()
    jobs = list()
    for job in jobData:
        temp = dict()

        temp['jobID'] = job.get('job_id')
        temp['jobFinished'] = jobFinished

        temp['visitDate'] = job.get('visit_date')
        temp['jobPrice'] = int(job.get('job_price'))
        temp['jobDescription'] = job.get('job_description')

        jobs.append(temp)

    payload['customerID'] = customerID
    payload['jobData'] = jobs

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")
