from flask import Blueprint, render_template, make_response, request, g
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.secret import backendData

front = Blueprint('addNewReserve', __name__, url_prefix='/reserves')
@front.route('/customer/<customerID>', methods=['GET'])
@tokenVerify
def addNewReservePage(customerID):
    accessToken = g.get('accessToken')

    url = backendData['ADDR'] + '/customers/' + customerID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.get(url=url, headers=headers)

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    # 손님 id는 url에서 받음
    data = json.loads(req.text)
    customerData = data.get('customerData')[0]

    temp = make_response(render_template('reserve-add.html', customerData=customerData, customerID=customerID))
    temp.set_cookie('accessToken', g.get('accessToken'), max_age=timedelta(hours=3), httponly=True)
    return temp

@front.route('/customer/<customerID>', methods=['POST'])
@tokenVerify
def addNewJob(customerID):
    accessToken = g.get('accessToken')

    customerData = {'customerID': customerID}

    reserveType = request.form.getlist('reserveType')    
    reserveTime = request.form.get('reserveTime')

    reserveData = dict()
    reserveData['customerID'] = customerID
    reserveData['reserveType'] = reserveType
    reserveData['reserveTime'] = reserveTime

    # 백엔드와 통신, 데이터 등록
    url = backendData['ADDR'] + '/reserves/customer/' + customerID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.post(url=url, headers=headers, data=reserveData)

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    # 백엔드에서 손님 데이터 받아옴
    # 손님 id는 url에서 받음
    url = backendData['ADDR'] + '/customers/' + customerID
    req = request.get(url=url, headers=headers)

    data = json.loads(req.text)
    customerData = data.get('customerData')[0]

    temp = make_response(render_template('reserve-data.html', customerData=customerData, customerID=customerID, reserveData=reserveData))
    temp.set_cookie('accessToken', g.get('accessToken'), max_age=timedelta(hours=3), httponly=True)
    return temp