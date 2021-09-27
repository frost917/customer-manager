from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

import jwt
from config.secret import JWTSecret

# return Access token
def createAccessToken(userID: str, UUID: str, refTime = datetime.now()):
    payload = dict()
    payload['userID'] = userID
    payload['UUID'] = UUID

    payload["exp"] = refTime + timedelta(hours=3)
    payload["iat"] = refTime
    payload["sub"] = "access token"
    # payload["aud"] = userID

    token = jwt.encode(payload=payload, key=JWTSecret)
    return str(token)

# return RefreshToken
# To save redis
# refreshToken은 발급 후 3개월 뒤 파기
def createRefreshToken(refTime = datetime.now()):
    payload = dict()

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
        isAccesTokenExpired = True

    return isAccesTokenExpired

def isRefreshTokenValid(refreshToken):
    isRefreshTokenExpired = False

    # redis에 토큰 데이터 없으면 그냥 파기된거로
    import redisCustom
    redis = redisCustom.redisToken()
    if redis.getUserID(refreshToken) is None:
        isRefreshTokenExpired = True
    if redis.getUUID(refreshToken) is None:
        isRefreshTokenExpired = True

    return isRefreshTokenExpired

def tokenGetUserID(accessToken):
    from flask import Response
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
    
    result = decode.get('userID')
    return result

# return UUID
def tokenGetUUID(accessToken):
    from flask import Response
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
    
    result = decode.get('UUID')
    return result
