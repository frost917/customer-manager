from datetime import timedelta
from flask import Flask, g, request, Response, make_response, Blueprint
from flask.templating import render_template

import requests
import json

front = Blueprint('loginPage', __name__, url_prefix='/login')

@front.route('', methods=['GET'])
def loginPage():
    # 기존에 로그인 된 기록이 있는지 확인
    accessToken = request.cookies.get('accessToken')
    refreshToken = request.cookies.get('refreshToken')

    if accessToken is not None and refreshToken is not None:
        return render_template('''
        <script>alert("이미 로그인 되어있습니다.");</script>
        ''')
        
    # refreshToken이 있으면 accessToken만 따로 생성
    elif accessToken is None and refreshToken is not None:
        url = 'http://localhost:6000/auth/refresh'
        headers = {'refreshToken': refreshToken}
        req = requests.post(url=url, headers=headers)

        if 500 <= req.status_code and req.status_code <= 599:
            return render_template('''<script>alert("서버 에러");</script>''')
        
        loginData = json.loads(req.text)
        accessToken = loginData.get('accessToken')

        loginResult = make_response(render_template('''<script>alert("로그인 성공");</script>'''))
        loginResult.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3))

        return loginResult

    elif accessToken is None and refreshToken is None:
        return render_template('login.html')