from dataCheck import customerDataCheck, jobDataCheck
import json

from flask import Blueprint, Response
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify

manager = Blueprint('getJobHistory', __name__, url_prefix='/jobs')

# 특정 시술 id의 데이터를 불러옴
@manager.route('/<jobID>', methods=['GET'])
@tokenVerify
def getJobHistory(jobID):
    database = PostgresControll()

    jobList = database.getJobListFromJobID(jobID=jobID)
    jobHistory = database.getJobHistorySpec(jobID=jobID)
    jobFinished = database.getJobFinishedArray(jobID=jobID)

    customerData = database.getCustomerData(customerID=jobList.get('customer_id'))

    if len(jobList) == 0:
        from msg.jsonMsg import jobNotFound
        return Response(jobNotFound(), status=404, content_type="application/json; charset=UTF-8")

    payload = dict()
    array = list()
    temp = dict()

    # 손님 데이터 패키징
    temp['customerID'] = jobList.get('customer_id')
    temp['customerName'] = customerData.get('customer_name')
    temp['phoneNumber'] = customerData.get('phone_number')
    array.append(temp)
    
    payload['customerData'] = array

    # 시술 데이터 패키징
    temp = dict()
    temp['jobID'] = jobID

    array = dict()
    for finished in jobFinished:
        array[int(finished.get('type_id'))] = finished.get('job_name')
    temp['jobFinished'] = array

    temp['visitDate'] = jobList.get('visit_date').strftime('%Y-%m-%d')
    temp['jobPrice'] = int(jobHistory.get('job_price'))
    temp['jobDescription'] = jobHistory.get('job_description')

    payload['jobData'] = temp

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")

