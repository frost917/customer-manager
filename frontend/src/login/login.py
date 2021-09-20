from datetime import timedelta
from flask import request, make_response, Blueprint

import requests
import json

from config.backendData import backendData
from statusCodeParse import parseStatusCode
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

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
    req = requests.post(url=url, headers=headers, data=data, verify=False)

    if 200 <= req.status_code and req.status_code <= 299:
        loginData = json.loads(req.text)
        accessToken = loginData.get('accessToken')
        refreshToken = loginData.get('refreshToken')

        if accessToken is None or refreshToken is None:
            return """<script>
            alert("아이디 또는 비밀번호가 잘못되었습니다");
            location.href="/login";
            </script>"""

        loginResult = make_response("""<script>
        location.href="/"
        </script>""")
        loginResult.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
        loginResult.set_cookie('refreshToken', refreshToken, max_age=timedelta(hours=4320), httponly=True)

        return loginResult

    else:
        print(json.loads(req.text))
        return parseStatusCode(req.status_code)