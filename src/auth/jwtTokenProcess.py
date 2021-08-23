from datetime import datetime, timedelta

import jwt
from config import secret


# return Access token
def createAccessToken(userID, UUID):
    payload = dict()
    payload['userID'] = userID
    payload['UUID'] = UUID

    # 토큰 생성의 기준이 되는 시간
    refTime = datetime.now()

    payload["exp"] = refTime + timedelta(hours=3)
    payload["iat"] = refTime
    payload["sub"] = "access token"
    payload["aud"] = userID

    token = jwt.encode(payload=payload, key=secret.JWTSecret)
    return str(token)

# return RefreshToken
# To save redis
# refreshToken은 발급 후 3개월 뒤 파기
def createRefreshToken():
    payload = dict()
    # 토큰 생성의 기준이 되는 시간
    refTime = datetime.now()

    payload["exp"] = refTime + timedelta(hours=3)
    payload["iat"] = refTime
    payload["sub"] = "refresh token"

    token = jwt.encode(payload=payload, key=secret.JWTSecret)
    return str(token)

# 토큰의 유효성을 검사함.
# access token이나 refresh token 둘 다 만료되거나
# refresh token이 위변조되었을 경우 토큰을 파기함 
def isAccessTokenValid(accessToken):
    isAccesTokenExpired = False

    try:
        jwt.decode(accessToken, secret.JWTSecret)
    except jwt.ExpiredSignatureError:
        isAccesTokenExpired = True
    except jwt.DecodeError():
        return None

    return isAccesTokenExpired

def isRefreshTokenValid(refreshToken):
    isRefreshTokenExpired = False

    try:
        jwt.decode(refreshToken, secret.JWTSecret)
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
    except jwt.DecodeError():
        pass

    return isRefreshTokenExpired

# refresh token 갱신에 필요함
def tokenGetUserID(accessToken):
    # 토큰 디코딩 후 에러 발생시
    # None 반환
    try:
        decode = jwt.decode(accessToken, secret.JWTSecret)
    except jwt.InvalidSignatureError:
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
    return str(decode.get("UUID"))
# return userID | UUID
def tokenGetUUID(accessToken):

    # 토큰 디코딩 후 에러 발생시
    # None 반환
    try:
        decode = jwt.decode(accessToken, secret.JWTSecret)
    except jwt.InvalidSignatureError:
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
    return str(decode.get("UUID"))
