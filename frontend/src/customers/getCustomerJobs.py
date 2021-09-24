from flask import render_template, Blueprint, request

import json, requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

front = Blueprint('customerJobData', __name__, url_prefix='/customers')
@front.route('/<customerID>/jobs', methods=['GET'])
@tokenVerify
def customerJobData(customerID):
    accessToken = request.cookies.get('accessToken')

    url = backendData['ADDR']
    customerUrl = url + '/jobs/customer/' + customerID
    headers = {'Content-Type': 'charset=utf-8', 'Authorization': accessToken}
    req = requests.get(url=customerUrl, headers=headers, verify=backendData['CA_CERT'])

    if req.status_code != 200:
        return parseStatusCode(req)

    data = json.loads(req.text)
    customerData = data.get('customerData')
    jobData = data.get('jobData')

    result = render_template('customer-data.html', customerData=customerData,customerID=customerID,  jobData=jobData)
    return result