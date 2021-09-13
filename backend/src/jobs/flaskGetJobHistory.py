from dataCheck import customerDataCheck
import json

from flask import Blueprint, Response
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

manager = Blueprint('getJobHistory', __name__, url_prefix='/jobs')

# 특정 작업 id의 데이터를 불러옴
@manager.route('/job/<jobID>', methods=['GET'])
@tokenVerify
@dataParsing
@customerDataCheck
def getJobHistory(jobID):
    database = PostgresControll()

    job = database.getJobHistory(jobID=jobID)

    if job is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype='application/json',content_type='application/json')

    payload = dict()

    temp = dict()

    temp['jobFinished'] = list()
    for jobType in job.get('job_finished'):
        temp['jobFinished'].append(jobType)

    temp['visitDate'] = job.get('visit_date')
    temp['jobPrice'] = int(job.get('job_price'))
    temp['jobDescription'] = job.get('job_description')

    jobID = job.get('job_id')
    payload[jobID] = temp

    return Response(json.dumps(payload), status=200, mimetype='application/json', content_type='application/json')

