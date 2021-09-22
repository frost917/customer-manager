from flask import (g, Blueprint, render_template, request, redirect, make_response)
from datetime import timedelta

import json, requests

from login.loginVerify import tokenVerify
from config.backendData import backendData
from statusCodeParse import parseStatusCode

front = Blueprint('addNewCustomer', __name__, url_prefix='/customers')
@front.route('/create', methods=['GET'])
@tokenVerify
def addNewCustomerPage():
    result = make_response(render_template('customer-add.html'))
    result.set_cookie('accessToken', g.get('accessToken'), max_age=timedelta(hours=3), httponly=True)
    result.set_cookie('refreshToken', g.get('refreshToken'), max_age=timedelta(hours=4320), httponly=True)
    return result

@front.route('/create', methods=['POST'])
@tokenVerify
def addNewCustomer():
    accessToken = g.get('accessToken')

    customerName = request.form.get('customerName')
    phoneNumber = request.form.get('phoneNumber')

    customerData = { 'customerName': customerName, 'phoneNumber': phoneNumber }
    payload = { 'customerData': [customerData] }

    url = backendData['ADDR'] + '/customers'
    headers = {'content-type': 'application/json; charset=UTF-8', 'Authorization': accessToken}
    req = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=False)

    if req.status_code != 200:
        return parseStatusCode(req)

    customerID = json.loads(req.text).get('customerData')[0].get('customerID')

    result = make_response(redirect('/customers/' + customerID + '/jobs'))
    result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
    result.set_cookie('refreshToken', g.get('refreshToken'), max_age=timedelta(hours=4320), httponly=True)
    return result