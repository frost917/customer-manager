from flask import Blueprint, render_template, g, make_response
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

front = Blueprint('getJobData', __name__, url_prefix='/jobs')
@front.route('/<jobID>', methods=['GET'])
@tokenVerify
def getJobData(jobID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR'] + '/jobs/' + jobID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.get(url=url, headers=headers, verify=backendData['CA_CERT'])

    if req.status_code != 200:
        return parseStatusCode(req)

    data = json.loads(req.text)
    customerData = data.get('customerData')[0]
    jobData = data.get('jobData')

    customerID = customerData.get('customerID')

    result = make_response(render_template('job-data.html', customerData=customerData, jobData=jobData, customerID=customerID))
    result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
    result.set_cookie('refreshToken', g.get('refreshToken'), max_age=timedelta(hours=4320), httponly=True)
    return result