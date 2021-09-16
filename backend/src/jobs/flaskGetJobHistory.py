from dataCheck import customerDataCheck, jobDataCheck
import json

from flask import Blueprint, Response
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

manager = Blueprint('getJobHistory', __name__, url_prefix='/jobs')

# 특정 작업 id의 데이터를 불러옴
@manager.route('/job/<jobID>', methods=['GET'])
@tokenVerify
@customerDataCheck
@jobDataCheck
def getJobHistory(jobID):
    database = PostgresControll()

    jobData = database.getJobHistorySpec(jobID=jobID)
    jobFinished = database.getJobFinishedArray(jobID=jobID)
    customerData = database.getCustomerFromJobID(jobID=jobID)

    print(jobData)
    print(jobFinished)
    print(customerData)

    payload = dict()
    array = list()
    temp = dict()

    # 손님 데이터 패키징
    temp['customerID'] = customerData.get('customer_id')
    temp['customerName'] = customerData.get('customer_name')
    temp['phoneNumber'] = customerData.get('phone_number')
    array.append(temp)
    
    # 작업 데이터 패키징
    temp = dict()
    temp['jobID'] = jobID
    jobs = list
    for finished in jobFinished:
        jobs.append(finished.get('type_id'))
    temp['visitDate'] = jobData.get('visit_date').strftime('%Y-%m-%d')
    temp['jobPrice'] = int(jobData.get('job_price'))
    temp['jobDescription'] = jobData.get('job_description')

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")

