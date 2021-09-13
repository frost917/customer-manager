﻿from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import jwt
import os
JWTSecret = os.getenv('secret')

# return Access token
def createAccessToken(userID: str, UUID: str):
    payload = dict()
    payload['userID'] = userID
    payload['UUID'] = UUID

    # 토큰 생성의 기준이 되는 시간
    refTime = datetime.now()

    payload["exp"] = refTime + timedelta(hours=3)
    payload["iat"] = refTime
    payload["sub"] = "access token"
    # payload["aud"] = userID

    token = jwt.encode(payload=payload, key=JWTSecret)
    return str(token)

# return RefreshToken
# To save redis
# refreshToken은 발급 후 3개월 뒤 파기
def createRefreshToken():
    payload = dict()
    # 토큰 생성의 기준이 되는 시간
    refTime = datetime.now()

    payload["exp"] = refTime + relativedelta(months=3)
    payload["iat"] = refTime
    payload["sub"] = "refresh token"

    token = jwt.encode(payload=payload, key=JWTSecret)
    return str(token)

# 토큰의 유효성을 검사함.
# access token이나 refresh token 둘 다 만료되거나
# refresh token이 위변조되었을 경우 토큰을 파기함 
def isAccessTokenValid(accessToken):
    isAccesTokenExpired = False

    try:
        jwt.decode(accessToken, JWTSecret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        isAccesTokenExpired = True
    except jwt.DecodeError:
        pass

    return isAccesTokenExpired

def isRefreshTokenValid(refreshToken):
    isRefreshTokenExpired = False

    try:
        jwt.decode(refreshToken, JWTSecret, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return None
    except jwt.InvalidSignatureError:
        # 시그니쳐 에러가 발생한 경우
        # refresh token이 위변조 된 것으로 간주
        from redisCustom import redisToken
        redisToken.delRefreshToken(refreshToken=refreshToken)
        return None
    except jwt.ExpiredSignatureError:
        isRefreshTokenExpired = True
    except jwt.DecodeError:
        pass

    return isRefreshTokenExpired

def tokenGetUserID(accessToken):
    from flask import Response
    import json
    # 토큰 디코딩 후 에러 발생시
    # None 반환
    try:
        decode = jwt.decode(jwt=accessToken, key=JWTSecret, algorithms=['HS256'])
    except jwt.InvalidSignatureError:
        return None
    except jwt.ExpiredSignatureError:
        return Response
    except jwt.InvalidTokenError:
        return None
    
    return decode.get("userID")

# return UUID
def tokenGetUUID(accessToken):
    from flask import Response
    # 토큰 디코딩 후 에러 발생시
    # None 반환
    try:
        print('try get uuid')
        decode = jwt.decode(jwt=accessToken, key=JWTSecret, algorithms=['HS256'])
    except jwt.InvalidSignatureError:
        return None
    except jwt.ExpiredSignatureError:
        return Response
    except jwt.InvalidTokenError:
        return None
    
    return decode.get("UUID")