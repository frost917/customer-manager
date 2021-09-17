from datetime import timedelta
from flask import Flask, g, request, Response, make_response, Blueprint
from flask.templating import render_template

import requests
import json

front = Blueprint('login', __name__, url_prefix='/login')

@front.route('', methods=['POST'])
def login():
    userID = request.form.get('userID')
    passwd = request.form.get('passwd')

    # 로그인 페이지와 연동
    url = 'http://localhost:6000/auth'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = json.dumps({'userID': userID, 'passwd': passwd})
    req = requests.get(url=url, headers=headers, data=data)

    if 200 <= req.status_code and req.status_code <= 299:
        loginData = json.loads(req.text)
        accessToken = loginData.get('accessToken')
        refreshToken = loginData.get('refreshToken')

        if accessToken is None or refreshToken is None:
            return render_template('''
            <script>alert("아이디 또는 비밀번호가 잘못되었습니다");</script>
            ''')

        loginResult = make_response(render_template('''<script>alert("로그인 성공");</script>'''))
        loginResult.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3))
        loginResult.set_cookie('refreshToken', refreshToken, max_age=timedelta(hours=4320))

        return loginResult

    elif 500 <= req.status_code and req.status_code <= 599:
        return render_template('''
        <script>alert("서버 에러");</script>
        ''')

    elif 400 <= req.status_code and req.status_code <= 499:
        return render_template('''
        <script>alert("아이디 또는 비밀번호가 잘못되었습니다");</script>
        ''')