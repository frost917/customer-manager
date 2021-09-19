from flask import Blueprint, render_template, make_response, g
import json
import requests
from datetime import timedelta

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.secret import backendData

front = Blueprint('getReserveData', __name__, url_prefix='/reserves')
@front.route('/<reserveID>', methods=['GET'])
@tokenVerify
def getReserveData(reserveID):
    accessToken = g.get('accessToken')

    # 예약 id로 데이터 불러오기
    url = backendData['ADDR']
    reserveUrl = url + '/reserves/' + reserveID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    reserveReq = requests.get(url=reserveUrl, headers=headers)

    if reserveReq.status_code != 200:
        return parseStatusCode(reserveReq.status_code)

    data = json.loads(reserveReq.text)
    reserveData = data.get('reserveData')[0]

    print(reserveData)

    # 날짜 데이터는 일자 / 시간 으로 분리
    reserveDate = reserveData['reserveTime'].split()[0]
    reserveTime = reserveData['reserveTime'].split()[1]

    customerID = reserveData.get('customerID')
    customerUrl = url + '/customers/' + customerID
    customerReq = requests.get(url=customerUrl, headers=headers)

    if customerReq.status_code != 200:
        return parseStatusCode(customerReq.status_code)

    data = json.loads(customerReq.text)
    customerData = data.get('customerData')[0]
    customerID = customerData.get('customerID')

    result = make_response(
        render_template('reserve-data.html', 
            customerData=customerData, 
            reserveData=reserveData,
            reserveDate=reserveDate,
            reserveTime=reserveTime, 
            customerID=customerID)
    )
    result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)

    return result