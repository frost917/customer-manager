from flask import Blueprint, render_template, make_response, g
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.secret import backendData

front = Blueprint('getReserveData', __name__, url_prefix='/reserve')
@front.route('/<reserveID>', methods=['GET'])
@tokenVerify
def getReserveData(reserveID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR']
    reserveUrl = url + '/reserves/' + reserveID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    reserveReq = requests.get(url=reserveUrl, headers=headers)

    if reserveReq.status_code != 200:
        return parseStatusCode(reserveReq.status_code)

    data = json.loads(reserveReq.text)
    reserveData = data.get('reserveData')[0]

    customerID = reserveData.get('customerID')
    customerUrl = url + '/customers/' + customerID
    customerReq = requests.get(url=customerUrl, headers=headers)

    if customerReq.status_code != 200:
        return parseStatusCode(customerReq.status_code)

    data = json.loads(customerReq.text)
    customerData = data.get('customerData')[0]
    customerID = customerData.get('customerID')

    result = make_response(render_template('reserve-data.html', customerData=customerData, reserveData=reserveData, customerID=customerID))
    result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)

    return result