from flask import render_template, g, Blueprint

import json, requests

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
    req = requests.get(url=customerUrl, headers=headers, verify=False)

    if req.status_code != 200:
        return parseStatusCode(req)

    data = json.loads(req.text)
    customerData = data.get('customerData')
    jobData = data.get('jobData')

    result = g.get('response')
    result.response = render_template('customer-data.html', customerData=customerData,customerID=customerID,  jobData=jobData)
    return result