from flask import Blueprint, request, redirect
import json, requests

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

front = Blueprint('updateReserveData', __name__, url_prefix='/reserves')
@front.route('/<reserveID>', methods=['POST'])
@tokenVerify
def updateReserveData(reserveID):
    accessToken = request.cookies.get('accessToken')

    reserveType = request.form.getlist('reserveType')    
    reserveDate = request.form.get('reserveDate')
    reserveTime = request.form.get('reserveTime')

    reserveData = dict()
    reserveData['reserveID'] = reserveID
    reserveData['reserveType'] = reserveType
    reserveData['reserveTime'] = reserveDate + ' ' + reserveTime

    payload = {'reserveData': [ reserveData ]}

    # 백엔드와 통신, 데이터 업데이트
    url = backendData['ADDR'] + '/reserves'
    headers = {'content-type': 'application/json; charset=UTF-8', 'Authorization': accessToken}
    req = requests.put(url=url, headers=headers, data=json.dumps(payload), verify=backendData['CA_CERT'])

    if req.status_code != 200:
        return parseStatusCode(req=req)

    # 업데이트 후 데이터 열람 페이지로 이동
    result = redirect('/reserves/' + reserveID)
    return result