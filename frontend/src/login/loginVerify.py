from typing import Literal
from flask import request, redirect, make_response
from functools import wraps
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

from statusCodeParse import parseStatusCode
from getNewTokens import tokenRefreshing
from config.backendData import backendData
from login.cookiePackage import setAccessTokenCookie, setRefreshTokenCookie, destroyCookie

# 토큰 살아있는지 확인
def tokenVerify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 토큰을 g 변수로 넘겨서 로그인 토큰 파기된 경우에 대처하기
        accessToken = request.cookies.get('accessToken')
        refreshToken = request.cookies.get('refreshToken')
        tokenTime = request.cookies.get('tokenTime')

        # 둘 다 없으면 로그인 페이지로 넘김
        if accessToken is None and refreshToken is None and tokenTime is None:
            result = redirect('/login')
            return result

        # 토큰 파기됐을 경우 이곳으로 데이터를 넘겨서
        # 다시 토큰을 받아올 수 있게끔 유도
        elif accessToken is not None and refreshToken is not None:
            url = backendData['ADDR']
            headers = {'Authorization': accessToken}
            req = requests.get(url=url, headers=headers, verify=backendData['CA_CERT'])
        
            if 200 <= req.status_code and req.status_code <= 299:
                # 군대 이슈 회피를 위한 refreshToken 갱신
                # 로그인 일자로부터 2주 이상 지났으면 자동 갱신
                compTime = datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(weeks=2)
                if compTime < datetime.now():
                    tokenData = tokenRefreshing(accessToken, refreshToken=None)

                    result = setRefreshTokenCookie(tokenData=tokenData)
                    return result

            # 토큰 파기된 경우 재생성 후 원래 가려던 곳으로 이동
            elif req.status_code == 401:
                tokenData = tokenRefreshing(accessToken=None, refreshToken=refreshToken)
                
                if tokenData is False:
                    from login.cookiePackage import destroyCookie
                    result = destroyCookie()

                # tokenData가 dict일 경우 올바른 응답이므로
                # 그대로 쿠키에 토큰 등록하고 리로딩
                elif tokenData is dict:
                    result = setAccessTokenCookie(tokenData=tokenData)

                # Literal로 반환되었을 경우 백엔드 에러
                elif tokenData is Literal:
                    result = tokenData            
                
                return result

            else:
                result =  parseStatusCode(req)
                return result

        # accessToken이 만료되었을 경우 재발급
        elif accessToken is None and refreshToken is not None:
            tokenData = tokenRefreshing(accessToken, refreshToken)

            # accessToken은 dict형식으로 반환함
            if tokenData is False:
                result = destroyCookie()
            
            # tokenData가 dict일 경우 올바른 응답이므로
            # 그대로 쿠키에 토큰 등록하고 리로딩
            elif tokenData is dict:
                result = setAccessTokenCookie(tokenData=tokenData)

            # Literal로 반환되었을 경우 잘못된 값임
            elif tokenData is Literal:
                result = tokenData      

            return result

        # refreshToken이 없는 경우 accessToken을 이용해
        # refreshToken을 재생성
        elif accessToken is not None and refreshToken is None:
            tokenData = tokenRefreshing(accessToken, refreshToken)

            # accessToken은 dict형식으로 반환함
            if tokenData is False:
                result = destroyCookie()
            
            # Literal로 반환되었을 경우 잘못된 값임
            elif tokenData is Literal:
                result = tokenData   

            # 반환값이 dict인 경우
            elif tokenData is dict:
                result = setRefreshTokenCookie(tokenData=tokenData)

            return result

        # tokenTime 쿠키 값이 없는 경우 refreshToken을 재발급
        # accessToken이 파기되어 로그아웃 되는 것을 막기 위해
        # 토큰 재발급 우선순위는 맨 뒤로 미룬다.
        elif tokenTime is None:
            tokenData = tokenRefreshing(accessToken, refreshToken=None)

            # 반환값이 dict인 경우
            if tokenData is dict:
                result = setRefreshTokenCookie(tokenData=tokenData)

            # accessToken은 dict형식으로 반환함
            elif tokenData is False:
                result = destroyCookie()
            
            # Literal로 반환되었을 경우 잘못된 값임
            elif tokenData is Literal:
                result = tokenData

            return result

        return func(*args, **kwargs)
    return wrapper