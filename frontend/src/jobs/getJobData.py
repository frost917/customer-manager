from flask import Blueprint, render_template, g
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from returnResponse import makeResponse
from config.backendData import backendData

front = Blueprint('getJobData', __name__, url_prefix='/jobs')
@front.route('/<jobID>', methods=['GET'])
@tokenVerify
@makeResponse
def getJobData(jobID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR'] + '/jobs/' + jobID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.get(url=url, headers=headers, verify=False)

    if req.status_code != 200:
        return parseStatusCode(req)

    data = json.loads(req.text)
    customerData = data.get('customerData')[0]
    jobData = data.get('jobData')

    customerID = customerData.get('customerID')

    result = render_template('job-data.html', customerData=customerData, jobData=jobData, customerID=customerID)
    return result