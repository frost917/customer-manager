from flask import Blueprint, render_template, make_response, request, g
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.secret import backendData

front = Blueprint('addNewReserve', __name__, url_prefix='/reserves')
@front.route('/customer/<customerID>', methods=['PUT'])
@tokenVerify
def updateReserveData(customerID):
    accessToken = g.get('accessToken')

    customerData = {'customerID': customerID}

    reserveType = request.form.getlist('reserveType')    
    reserveDate = request.form.get('reserveDate')
    reserveTime = request.form.get('reserveTime')

    reserveData = dict()
    reserveData['customerID'] = customerID
    reserveData['reserveType'] = reserveType
    reserveData['reserveTime'] = reserveDate + ' ' + reserveTime

    payload = {'reserveData': [ reserveData ]}

    # 백엔드와 통신, 데이터 업데이트
    url = backendData['ADDR'] + '/reserves/customer/' + customerID
    headers = {'content-type': 'application/json; charset=UTF-8', 'Authorization': accessToken}
    req = requests.put(url=url, headers=headers, data=json.dumps(payload))

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    # 백엔드에서 손님 데이터 받아옴
    # 손님 id는 url에서 받음
    url = backendData['ADDR'] + '/customers/' + customerID
    req = requests.get(url=url, headers=headers)

    data = json.loads(req.text)
    customerData = data.get('customerData')[0]

    temp = make_response(render_template('reserve-data.html', customerData=customerData, customerID=customerID, reserveData=reserveData))
    temp.set_cookie('accessToken', g.get('accessToken'), max_age=timedelta(hours=3), httponly=True)
    return temp