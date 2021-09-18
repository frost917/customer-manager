from flask import Blueprint, render_template, make_response, request, g
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.secret import backendData

front = Blueprint('addNewJob', __name__, url_prefix='/jobs')
@front.route('/<customerID>/job', methods=['GET'])
@tokenVerify
def addNewJobPage(customerID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR'] + '/customers/' + customerID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.get(url=url, headers=headers)

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    data = json.loads(req.text)
    customerData = data.get('customerData')[0]

    temp = make_response(render_template('job-add.html', customerData=customerData, customerID=customerID))
    temp.set_cookie('accessToken', g.get('accessToken'), max_age=timedelta(hours=3))
    return temp

@front.route('/<customerID>/job', methods=['POST'])
@tokenVerify
def addNewJob(customerID):
    accessToken = g.get('accessToken')
    payload = dict()

    customerID = request.form.get('customerID')

    jobFinished = request.form.getlist('jobFinished')
    jobPrice = request.form.get('jobPrice')
    jobDescription = request.form.get('jobDescription')

    jobData = dict()
    jobData['jobFinished'] = jobFinished
    jobData['jobPrice'] = jobPrice
    jobData['jobDescription'] = jobDescription

    temp = [jobData]
    payload['jobData'] = temp

    url = 'http://localhost:6000'
    customerUrl = url + '/jobs'
    headers = {'Content-Type': 'charset=utf-8', 'Authorization': accessToken}
    req = requests.post(url=customerUrl, headers=headers)

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    data = json.loads(req.text)
    jobData = data.get('jobData')[0]
    jobID = jobData.get('jobID')

    temp = make_response(render_template('customer-data.html'))
    temp.set_cookie('accessToken', g.get('accessToken'), max_age=timedelta(hours=3))