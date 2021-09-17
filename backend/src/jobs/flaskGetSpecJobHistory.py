from dataCheck import customerDataCheck
import json

from auth.flaskAuthVerify import tokenVerify
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('getSpecJobHistory', __name__, url_prefix='/jobs')

# 특정 고객의 모든 작업 기록을 불러옴
@manager.route('/customer/<customerID>', methods=['GET'])
@tokenVerify
def getJobHistory(customerID):
    database = PostgresControll()

    customerData = database.getCustomerData(customerID=customerID)
    if len(customerData) == 0:
        from msg.jsonMsg import customerNotFound
        return Response(customerNotFound(), status=404, content_type="application/json; charset=UTF-8")

    jobData = database.getJobsFromCustomerID(customerID=customerID)

    if jobData is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    payload = dict()
    jobs = list()
    for job in jobData:
        temp = dict()
        jobID = job.get('job_id')

        temp['jobID'] = jobID
        jobFinished = database.getJobFinishedArray(jobID=jobID)
        if jobFinished is None:
            from msg.jsonMsg import databaseIsGone
            return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

        # 반환 타입이 ReadDictRow라서 dict로 변환하는 작업
        array = dict()
        for finished in jobFinished:
            array[finished.get('type_id')] = finished.get('job_name')
        temp['jobFinished'] = array

        temp['visitDate'] = job.get('visit_date').strftime('%Y-%m-%d')
        if job.get('job_price') is None:
            temp['jobPrice'] = 0
        else: 
            temp['jobPrice'] = int(job.get('job_price'))
        temp['jobDescription'] = job.get('job_description')

        jobs.append(temp)

    temp = dict()
    temp['customerID'] = customerID
    temp['customerName'] = customerData.get('customer_name')
    temp['phoneNumber'] = customerData.get('phone_number')

    payload['customerData'] = temp
    payload['jobData'] = jobs

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")
