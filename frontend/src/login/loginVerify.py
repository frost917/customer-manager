from flask import request, redirect, make_response
from functools import wraps
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests, json

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
        tokenTime = request.cookies.get('tokenTime')

        # refreshToken 갱신 시간을 알 수 없으면 다시 받아오기
        if tokenTime is None:
            refreshToken = None

        # 토큰 파기됐을 경우 이곳으로 데이터를 넘겨서
        # 다시 토큰을 받아올 수 있게끔 유도
        if accessToken != None and refreshToken != None:
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
                    result.delete_cookie('tokenTime')
                    return result

                result = make_response("""<script>location.reload();</script>""")
                result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
                return result

            else:
                return parseStatusCode(req)

        # refreshToken이 있으면 accessToken만 따로 생성
        elif accessToken == None and refreshToken != None:
            accessToken = getAccessToken(accessToken, refreshToken)

            if accessToken is False:
                result = make_response(redirect('/login'))
                result.delete_cookie('accessToken')
                result.delete_cookie('refreshToken')
                return result

            result = make_response("""<script>location.reload();</script>""")
            result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
            return result

        # refreshToken이 없는 경우 accessToken을 이용해
        # refreshToken을 재생성
        elif accessToken != None and refreshToken == None:
            tokenData = getRefreshToken(accessToken, refreshToken)
            refreshToken = tokenData.get('refreshToken')
            tokenTime = tokenData.get('tokenTime')
            expireTime = int(round(tokenData.get('expireTime')))

            if tokenData is False:
                result = make_response(redirect('/login'))
                result.delete_cookie('accessToken')
                result.delete_cookie('refreshToken')
                result.delete_cookie('tokenTime')
                return result

            result = make_response("""<script>location.reload();</script>""")
            result.set_cookie('refreshToken', refreshToken, max_age=expireTime, httponly=True)
            result.set_cookie('tokenTime', tokenTime, max_age=expireTime, httponly=True)
            return result

        # 둘 다 없으면 로그인 페이지로 넘김
        elif accessToken == None and refreshToken == None and tokenTime == None:
            return redirect('/login')

        # 군대 이슈 회피를 위한 refreshToken 갱신
        # 로그인 일자로부터 3개월 이상 지났으면 자동 갱신
        originTime = datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(months=3)
        if originTime < datetime.now():
            headers = {'accessToken': accessToken}
            refUrl = url + '/auth/refresh'
            req = requests.get(url=refUrl, headers=headers, verify=backendData['CA_CERT'])

            if req.status_code != 200:
                return parseStatusCode(req)

            tokenData = getRefreshToken(accessToken, refreshToken)

            refreshToken = tokenData.get('refreshToken')
            tokenTime = tokenData.get('tokenTime')
            expireTime = int(round(datetime.strftime(tokenData.get('expireTime'), '%Y-%m-%d %H:%M:%S.%f')))

            result = make_response("""<script>location.reload();</script>""")
            result.set_cookie('refreshToken', refreshToken, max_age=expireTime, httponly=True)
            result.set_cookie('tokenTime', tokenTime, max_age=expireTime, httponly=True)
            return result

        return func(*args, **kwargs)
    return wrapper

# def tokenSaving(func):
#     result = 