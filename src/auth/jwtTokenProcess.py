import jwt
from config import secret
from datetime import datetime, timedelta

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
def isTokenValid(accessToken, refreshToken):
    resultDict = dict()
    isAccesTokenExpired = False
    isRefreshTokenExpired = False

    try:
        jwt.decode(accessToken, secret.JWTSecret)  
    except jwt.InvalidSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except jwt.ExpiredSignatureError:
        isAccesTokenExpired = True
    except jwt.DecodeError():
        pass

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
        from redisCustom import redisToken
        redisToken.delRefreshToken(refreshToken=refreshToken)
    except jwt.DecodeError():
        pass

    resultDict["accessTokenExpired"] = isAccesTokenExpired
    resultDict["refreshTokenExpired"] = isRefreshTokenExpired

    return resultDict


# return userID | UUID
def decodeToken(accessToken, retResource):

    # 토큰 디코딩 후 에러 발생시
    # None 반환
    try:
        decode = jwt.decode(accessToken, secret.JWTSecret)
    except jwt.InvalidSignatureError:
        pass
    except jwt.ExpiredSignatureError:
        # TODO 토큰이 파기된 경우 토큰 갱신용 페이지로 이동해야함
        pass
    except jwt.InvalidTokenError:
        return None
    
    # retResource에 따라 반환하는 데이터 변동
    if retResource == "userID":
        return str(decode.get("userID"))
    elif retResource == "UUID":
        return str(decode.get("UUID"))
    else:
        return None
