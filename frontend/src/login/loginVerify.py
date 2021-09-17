from flask import request, make_response, g

import json
import requests
from functools import wraps
from datetime import timedelta

from statusCodeParse import parseStatusCode

# 토큰 살아있는지 확인
def tokenVerify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 토큰을 g 변수로 넘겨서 로그인 토큰 파기된 경우에 대처하기
        accessToken = request.cookies.get('accessToken')
        refreshToken = request.cookies.get('refreshToken')

        # 토큰 파기됐을 경우 이곳으로 데이터를 넘겨서
        # 다시 토큰을 받아올 수 있게끔 유도
        if accessToken is not None and refreshToken is not None:
            url = 'http://localhost:6000/'
            headers = {'accessToken': accessToken}
            req = requests.get(url=url, headers=headers)

            # 토큰 파기된 경우 재생성 후 원래 가려던 곳으로 이동
            if req.status_code == 401:
                headers = {'accessToken': accessToken, 'refreshToken': refreshToken}
                req = requests.get(url=url, headers=headers)

                loginData = json.loads(req.text)
                accessToken = loginData.get('accessToken')

            elif req.status_code != 200:
                return parseStatusCode(req.status_code)

            g.accessToken = accessToken

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

        return func(*args, **kwargs)
    return wrapper
