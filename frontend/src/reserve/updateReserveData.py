from flask import Blueprint, render_template, make_response, request, g
import json
import requests
from datetime import timedelta

from werkzeug.utils import redirect

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

front = Blueprint('updateReserveData', __name__, url_prefix='/reserves')
@front.route('/<reserveID>', methods=['POST'])
@tokenVerify
def updateReserveData(reserveID):
    accessToken = g.get('accessToken')

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
    req = requests.put(url=url, headers=headers, data=json.dumps(payload))

    if req.status_code != 200:
        return parseStatusCode(req.status_code)

    # 업데이트 후 데이터 열람 페이지로 이동
    temp = make_response(redirect('/reserves/' + reserveID))
    temp.set_cookie('accessToken', g.get('accessToken'), max_age=timedelta(hours=3), httponly=True)
    return temp