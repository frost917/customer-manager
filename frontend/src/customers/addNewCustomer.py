from flask import (Blueprint, render_template, request, redirect)

import json, requests

from login.loginVerify import tokenVerify
from config.backendData import backendData
from statusCodeParse import parseStatusCode

front = Blueprint('addNewCustomer', __name__, url_prefix='/customers')
@front.route('/create', methods=['GET'])
@tokenVerify
def addNewCustomerPage():
    result = render_template('customer-add.html')
    return result

@front.route('/create', methods=['POST'])
@tokenVerify
def addNewCustomer():
    accessToken = request.cookies.get('accessToken')

    customerName = request.form.get('customerName')
    phoneNumber = request.form.get('phoneNumber')

    customerData = { 'customerName': customerName, 'phoneNumber': phoneNumber }
    payload = { 'customerData': [customerData] }

    url = backendData['ADDR'] + '/customers'
    headers = {'content-type': 'application/json; charset=UTF-8', 'Authorization': accessToken}
    req = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=backendData['CA_CERT'])

    if req.status_code != 200:
        return parseStatusCode(req)

    customerID = json.loads(req.text).get('customerData')[0].get('customerID')

    result = redirect('/customers/' + customerID + '/jobs')
    return result