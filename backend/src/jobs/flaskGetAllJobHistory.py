import json

from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

manager = Blueprint('getAllJobHistory', __name__, url_prefix='/jobs')

@manager.route('', methods=['GET'])
@tokenVerify
@dataParsing
def getAllJobHistory():
    database = PostgresControll()

    UUID = g.get('UUID')
    jobData = database.getJobsDict(UUID=UUID)

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
