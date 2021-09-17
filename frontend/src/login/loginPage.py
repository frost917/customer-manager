from datetime import timedelta
from flask import Flask, g, request, Response, make_response, Blueprint
from flask.templating import render_template

import requests
import json

from statusCodeParse import parseStatusCode

front = Blueprint('loginPage', __name__, url_prefix='/login')

@front.route('', methods=['GET'])
def loginPage():
    # 기존에 로그인 된 기록이 있는지 확인
    accessToken = request.cookies.get('accessToken')
    refreshToken = request.cookies.get('refreshToken')

    # 토큰 파기됐을 경우 이곳으로 데이터를 넘겨서
    # 다시 토큰을 받아올 수 있게끔 유도
    if accessToken is not None and refreshToken is not None:
        url = 'http://localhost:6000/auth/refresh'
        headers = {'accessToken': accessToken, 'refreshToken': refreshToken}
        req = requests.post(url=url, headers=headers)

        if req.status_code != 200:
            return parseStatusCode(req.status_code)

        loginData = json.loads(req.text)
        accessToken = loginData.get('accessToken')

        loginResult = make_response("""<script>
        history.go(-2);
        </script>""")
        loginResult.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3))

        return loginResult

    # refreshToken이 있으면 accessToken만 따로 생성
    elif accessToken is None and refreshToken is not None:
        url = 'http://localhost:6000/auth/refresh'
        headers = {'refreshToken': refreshToken}
        req = requests.post(url=url, headers=headers)

        if req.status_code != 200:
            return parseStatusCode(req.status_code)
        
        loginData = json.loads(req.text)
        accessToken = loginData.get('accessToken')

        loginResult = make_response("""<script>
        history.go(-2);
        </script>""")
        loginResult.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3))

        return loginResult

    elif accessToken is not None and refreshToken is None:
        url = 'http://localhost:6000/auth/refresh'
        headers = {'accessToken': accessToken}
        req = requests.post(url=url, headers=headers)

        if req.status_code != 200:
            return parseStatusCode(req.status_code)

        loginResult = make_response("""<script>
        history.go(-2);
        </script>""")
        loginResult.set_cookie('refreshToken', refreshToken, max_age=timedelta(hours=4320))

    elif accessToken is None and refreshToken is None:
        return render_template('login.html')