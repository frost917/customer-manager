﻿from flask import Blueprint, render_template, redirect, request, g
import json, requests

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

front = Blueprint('addNewReserve', __name__, url_prefix='/reserves')
@front.route('/customer/<customerID>', methods=['GET'])
@tokenVerify
def addNewReservePage(customerID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR'] + '/customers/' + customerID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.get(url=url, headers=headers, verify=False)

    if req.status_code != 200:
        return parseStatusCode(req)

    # 손님 id는 url에서 받음
    data = json.loads(req.text)
    customerData = data.get('customerData')[0]

    result = g.get('response')
    result.response = render_template('reserve-add.html', customerData=customerData, customerID=customerID)
    return result

@front.route('/customer/<customerID>', methods=['POST'])
@tokenVerify
def addNewJob(customerID):
    accessToken = g.get('accessToken')

    reserveType = request.form.getlist('reserveType')    
    reserveDate = request.form.get('reserveDate')
    reserveTime = request.form.get('reserveTime')

    reserveData = dict()
    reserveData['customerID'] = customerID
    reserveData['reserveType'] = reserveType
    reserveData['reserveTime'] = reserveDate + ' ' + reserveTime

    payload = {'reserveData': [ reserveData ]}

    # 백엔드와 통신, 데이터 등록
    url = backendData['ADDR'] + '/reserves/customer/' + customerID
    headers = {'content-type': 'application/json; charset=UTF-8', 'Authorization': accessToken}
    req = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=False)

    if req.status_code != 200:
        return parseStatusCode(req)

    reserveID = json.loads(req.text).get('reserveData')[0].get('reserveID')
    
    result = g.get('response')
    result.response = redirect('/reserves/'+ reserveID)
    return result