from flask import request, redirect, make_response
from functools import wraps
from datetime import timedelta
import requests

from statusCodeParse import parseStatusCode
from getNewTokens import getAccessToken, getRefreshToken
from config.backendData import backendData

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
            url = backendData['ADDR']
            headers = {'Authorization': accessToken}
            req = requests.get(url=url, headers=headers, verify=backendData['CA_CERT'])
        
            if 200 <= req.status_code and req.status_code <= 299:
                pass

            # 토큰 파기된 경우 재생성 후 원래 가려던 곳으로 이동
            elif req.status_code == 401:
                accessToken = getAccessToken(accessToken, refreshToken)

                if accessToken is False:
                    result = make_response(redirect('/login'))
                    result.delete_cookie('accessToken')
                    result.delete_cookie('refreshToken')
                    return result

                result = make_response("""<script>location.reload();</script>""")
                result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
                result.set_cookie('refreshToken', refreshToken, max_age=timedelta(hours=4320), httponly=True)
                return result

            else:
                return parseStatusCode(req)

        # refreshToken이 있으면 accessToken만 따로 생성
        elif accessToken is None and refreshToken is not None:
            accessToken = getAccessToken(accessToken, refreshToken)

            if accessToken is False:
                result = make_response(redirect('/login'))
                result.delete_cookie('accessToken')
                result.delete_cookie('refreshToken')
                return result

            result = make_response("""<script>location.reload();</script>""")
            result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
            result.set_cookie('refreshToken', refreshToken, max_age=timedelta(hours=4320), httponly=True)
            return result

        # refreshToken이 없는 경우 accessToken을 이용해
        # refreshToken을 재생성
        elif accessToken is not None and refreshToken is None:
            refreshToken = getRefreshToken(accessToken, refreshToken)

            if refreshToken is False:
                result = make_response(redirect('/login'))
                result.delete_cookie('accessToken')
                result.delete_cookie('refreshToken')
                return result

            result = make_response("""<script>location.reload();</script>""")
            result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
            result.set_cookie('refreshToken', refreshToken, max_age=timedelta(hours=4320), httponly=True)
            return result

        # 둘 다 없으면 로그인 페이지로 넘김
        elif accessToken is None and refreshToken is None:
            return redirect('/login')

        return func(*args, **kwargs)
    return wrapper

# def tokenSaving(func):
#     result = 