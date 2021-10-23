from dateutil.relativedelta import relativedelta
from flask import request, make_response, Blueprint

import json, requests
from datetime import datetime, timedelta

from config.backendData import backendData
from statusCodeParse import parseStatusCode

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
        accessToken = loginData.get('accessToken')
        refreshToken = loginData.get('refreshToken')
        tokenTime = loginData.get('tokenTime')
        expireTime = datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(months=1)
        expireInt = int(expireTime.timestamp())

        if accessToken is None or refreshToken is None:
            return """<script>
            alert("아이디 또는 비밀번호가 잘못되었습니다");
            location.href="/login";
            </script>"""

        # 로그인시 인증용 토큰과 갱신용 토큰 생성
        # 군대 이슈 때문에 자동 로그인을 위한 refreshToken 재발급을 위한
        # 로그인 일자 생성
        result = make_response("""<script>
        location.href="/"
        </script>""")
        result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True, secure=True)
        result.set_cookie('refreshToken', refreshToken, max_age=expireInt, httponly=True, secure=True)
        result.set_cookie('tokenTime', tokenTime, max_age=expireInt, httponly=True, secure=True)

        return result

    # 401 반환시 로그인 할 데이터 없는 것
    elif req.status_code == 401:
        return """<script>
        alert("아이디 혹은 비밀번호가 잘못되었습니다");
        location.href="/login";
        </script>"""

    else:
        print(json.loads(req.text))
        return parseStatusCode(req)