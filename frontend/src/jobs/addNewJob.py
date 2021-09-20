from flask import Blueprint, render_template, make_response, request, g, redirect
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

front = Blueprint('addNewJob', __name__, url_prefix='/jobs')
@front.route('/customer/<customerID>', methods=['GET'])
@tokenVerify
def addNewJobPage(customerID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR'] + '/customers/' + customerID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.get(url=url, headers=headers, verify=False)

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    data = json.loads(req.text)
    customerData = data.get('customerData')[0]

    temp = make_response(render_template('job-add.html', customerData=customerData, customerID=customerID))
    temp.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
    return temp

@front.route('/customer/<customerID>', methods=['POST'])
@tokenVerify
def addNewJob(customerID):
    accessToken = g.get('accessToken')
    data = dict()

    # 시술 데이터 불러오기
    jobFinished = request.form.getlist('jobFinished')
    jobPrice = request.form.get('jobPrice')
    jobDescription = request.form.get('jobDescription')

    # 시술 데이터 패키징
    jobData = dict()
    jobData['jobFinished'] = jobFinished
    jobData['jobPrice'] = jobPrice
    jobData['jobDescription'] = jobDescription

    temp = [jobData]
    data['jobData'] = temp

    # 백엔드에 접근해서 새 시술기록 추가
    url = backendData['ADDR']
    jobAddUrl = url + '/jobs/' + customerID + '/job'
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': accessToken}
    req = requests.post(url=jobAddUrl, headers=headers, data=json.dumps(data), verify=False)

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    # 반환받은 jobID를 통해 시술 내역 불러오기
    data = json.loads(req.text)
    jobData = data.get('jobData')[0]
    jobID = jobData.get('jobID')

    result = make_response(redirect('/jobs/'+ jobID, code=302))
    result.set_cookie('accessToken', g.get('accessToken'), max_age=timedelta(hours=3), httponly=True)

    return result