from typing import Literal
from flask import request, redirect, make_response
from functools import wraps
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

from responseBuilder import buildResponse
from responseEnum import ResponseType

from statusCodeParse import parseStatusCode
from getNewTokens import tokenRefreshing
from config.backendData import backendData

# 토큰 살아있는지 확인
def tokenVerify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 토큰을 g 변수로 넘겨서 로그인 토큰 파기된 경우에 대처하기
        accessToken = request.cookies.get('accessToken')
        refreshToken = request.cookies.get('refreshToken')

        # 아무것도 없으면 로그인 페이지로
        if accessToken is None and refreshToken is None:
            return buildResponse(None, ResponseType.LOGIN)

        # 둘 중 하나가 없으면 갱신
        elif accessToken is None or refreshToken is None:
            newToken = tokenRefreshing(accessToken=accessToken, refreshToken=refreshToken)

            # None이 반환된거면 토큰 자체가 파기된 것
            if newToken.get('accessToken') is None or newToken.get('refreshToken') is None :
                return buildResponse(tokens=newToken, responseType = ResponseType.TOKENEXPIRE)

            return buildResponse(tokens=newToken, responseType = ResponseType.REFRESH)

        return func(*args, **kwargs)
    return wrapper