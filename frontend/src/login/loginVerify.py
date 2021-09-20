from flask import request, make_response, g, redirect

import json
import requests
from functools import wraps
from datetime import timedelta

from statusCodeParse import parseStatusCode
from config.backendData import backendData
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# 토큰 살아있는지 확인
def tokenVerify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 토큰을 g 변수로 넘겨서 로그인 토큰 파기된 경우에 대처하기
        accessToken = request.cookies.get('accessToken')
        refreshToken = request.cookies.get('refreshToken')

        refreshUrl = backendData['ADDR'] + '/auth/refresh'

        # 토큰 파기됐을 경우 이곳으로 데이터를 넘겨서
        # 다시 토큰을 받아올 수 있게끔 유도
        if accessToken is not None and refreshToken is not None:
            url = backendData['ADDR']
            headers = {'Authorization': accessToken}
            req = requests.get(url=url, headers=headers, verify=False)
        
            if 200 <= req.status_code and req.status_code <= 299:
                pass
            # 토큰 파기된 경우 재생성 후 원래 가려던 곳으로 이동
            elif req.status_code == 401:
                headers = {'accessToken': accessToken, 'refreshToken': refreshToken}
                req = requests.get(url=refreshUrl, headers=headers, verify=False)

                loginData = json.loads(req.text)
                accessToken = loginData.get('accessToken')
            
            # 검증 끝나면 g 변수로 넘김
            g.accessToken = accessToken

        # refreshToken이 있으면 accessToken만 따로 생성
        elif accessToken is None and refreshToken is not None:
            headers = {'refreshToken': refreshToken}
            req = requests.post(url=refreshUrl, headers=headers, verify=False)

            if req.status_code != 200:
                return parseStatusCode(req.status_code)
            
            loginData = json.loads(req.text)
            accessToken = loginData.get('accessToken')

            loginResult = make_response("""<script>
            history.go(-1);
            </script>""")
            loginResult.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)

            return loginResult

        # refreshToken이 없는 경우 accessToken을 이용해
        # refreshToken을 재생성
        elif accessToken is not None and refreshToken is None:
            headers = {'accessToken': accessToken}
            req = requests.post(url=refreshUrl, headers=headers, verify=False)

            if req.status_code != 200:
                return parseStatusCode(req.status_code)

            loginResult = make_response("""<script>
            history.go(-1);
            </script>""")
            loginResult.set_cookie('refreshToken', refreshToken, max_age=timedelta(hours=4320), httponly=True)

        # 둘 다 없으면 로그인 페이지로 넘김
        elif accessToken is None and refreshToken is None:
            return redirect('/login')

        return func(*args, **kwargs)
    return wrapper


# def tokenSaving(func):
#     result = 