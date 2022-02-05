from flask import request, make_response
from functools import wraps

from responseBuilder import buildResponse
from responseEnum import ResponseType

from getNewTokens import tokenRefreshing

# 토큰 살아있는지 확인
def tokenVerify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        accessToken = request.cookies.get('accessToken')
        refreshToken = request.cookies.get('refreshToken')

        # 아무것도 없으면 로그인 페이지로
        if accessToken is None and refreshToken is None:
            return buildResponse(None, ResponseType.LOGIN)

        # 둘 중 하나가 없으면 갱신
        elif accessToken is None or refreshToken is None:
            newToken = tokenRefreshing(accessToken=accessToken, refreshToken=refreshToken)
            accessToken = newToken.get('accessToken')
            refreshToken = newToken.get('refreshToken')

            # None이 반환된거면 토큰 자체가 파기된 것
            if newToken.get('accessToken') is None or newToken.get('refreshToken') is None :
                return buildResponse(responseType = ResponseType.TOKENEXPIRE)

            return buildResponse(responseType = ResponseType.REFRESH, accessToken=accessToken, refreshToken=refreshToken)

        return func(*args, **kwargs)
    return wrapper