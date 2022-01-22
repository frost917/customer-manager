from distutils.command.build import build
from lib2to3.pgen2 import token
from dateutil.relativedelta import relativedelta
from flask import request, make_response, Blueprint

import json, requests
from datetime import datetime, timedelta

from config.backendData import backendData
from login.responseBuilder import buildResponse
from login.responseEnum import ResponseType

front = Blueprint('login', __name__, url_prefix='/login')

@front.route('', methods=['POST'])
def login():
    userID = request.form.get('userID')
    passwd = request.form.get('passwd')

    if userID is None or passwd is None:
        return """<script>
        alert("아이디 또는 비밀번호를 입력해주세요");
        location.href="/login";
        </script>"""

    # 로그인 페이지와 연동
    url = backendData['ADDR'] + '/auth'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = json.dumps({'userID': userID, 'passwd': passwd})
    req = requests.post(url=url, headers=headers, data=data, verify=backendData['CA_CERT'])

    if 200 <= req.status_code and req.status_code <= 299:
        loginData = json.loads(req.text)
        tokens = dict()

        tokens['accessToken'] = loginData.get('accessToken')
        tokens['refreshToken'] = loginData.get('refreshToken')

        if tokens['accessToken'] is None or tokens['refreshToken'] is None:
            responseType = ResponseType.ACCOUNTERROR
        else:
            responseType = ResponseType.LOGIN

    # 401 반환시 로그인 할 데이터 없는 것
    elif req.status_code == 401:
        responseType = ResponseType.ACCOUNTERROR

    else:
        print(json.loads(req.text))
        responseType = ResponseType.ERROR

    return buildResponse(tokens, responseType)