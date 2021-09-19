import json

from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify

manager = Blueprint('getAllJobHistory', __name__, url_prefix='/jobs')

@manager.route('', methods=['GET'])
@tokenVerify
def getAllJobHistory():
    database = PostgresControll()

    UUID = g.get('UUID')
    jobList = database.getAllJobs(UUID=UUID)

    if jobList is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    elif len(jobList) == 0:
        from msg.jsonMsg import jobNotFound
        return Response(jobNotFound(), status=404, content_type="application/json; charset=UTF-8")

    jobHistories = list()
    jobFinished = list()

    # 받아온 jobID로 job_history 테이블과 job_finished 테이블 순회
    # 에러 발생시 작업 중단 및 500 에러
    for jobs in jobList:
        jobID = jobs.get('job_id')
        history = database.getJobHistorySpec(jobID=jobID)
        finished = database.getJobFinishedArray(jobID=jobID)

        if history is None or finished is None:
            from msg.jsonMsg import databaseIsGone
            return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")
        
        jobHistories.append(history)
        jobFinished.append(finished)

    payload = dict()
    jobListTemp = list()

    for job, history  in zip(jobList, jobHistories):
        temp = dict()

        jobID = job.get('job_id')
        temp['jobID'] = jobID
        temp['jobFinished'] = jobFinished
        temp['visitDate'] = job.get('visit_date').strftime('%Y-%m-%d')
        temp['jobPrice'] = int(history.get('job_price'))
        temp['jobDescription'] = history.get('job_description')

        jobListTemp.append(temp)

    payload['jobData'] = jobListTemp

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")
