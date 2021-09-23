from flask import render_template, g, Blueprint, make_response

import json, requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

front = Blueprint('customerJobData', __name__, url_prefix='/customers')
@front.route('/<customerID>/jobs', methods=['GET'])
@tokenVerify
def customerJobData(customerID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR']
    customerUrl = url + '/jobs/customer/' + customerID
    headers = {'Content-Type': 'charset=utf-8', 'Authorization': accessToken}
    req = requests.get(url=customerUrl, headers=headers, verify=backendData['CA_CERT'])

    if req.status_code != 200:
        return parseStatusCode(req)

    data = json.loads(req.text)
    customerData = data.get('customerData')
    jobData = data.get('jobData')

    result = make_response(render_template('customer-data.html', customerData=customerData,customerID=customerID,  jobData=jobData))
    result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
    result.set_cookie('refreshToken', g.get('refreshToken'), max_age=timedelta(hours=4320), httponly=True)
    return result