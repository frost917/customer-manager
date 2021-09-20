from flask import Blueprint, render_template, make_response, g
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

front = Blueprint('getJobData', __name__, url_prefix='/jobs')
@front.route('/<jobID>', methods=['GET'])
@tokenVerify
def getJobData(jobID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR'] + '/jobs/' + jobID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.get(url=url, headers=headers, verify=False)

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    data = json.loads(req.text)
    customerData = data.get('customerData')[0]
    jobData = data.get('jobData')

    customerID = customerData.get('customerID')

    result = make_response(render_template('job-data.html', customerData=customerData, jobData=jobData, customerID=customerID))
    result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)

    return result