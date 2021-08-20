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
    return token

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
    return token

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


# return userData
def decodeToken(token):
    convDict = dict()
    convList = list()

    # 토큰 디코딩 후 에러 발생시
    # 해당 에러에 대응되는 JSON 객체 반환
    try:
        decode = jwt.decode(token, secret.JWTSecret)
    except jwt.ExpiredSignatureError:
        convDict['error'] = "TokenExpired"
        convDict['msg'] = "token is expired!"
        convList["failed"] = convDict
        return convList
    except jwt.InvalidSignatureError:
        pass
    except jwt.InvalidTokenError:
        convDict['error'] = "TokenInvalid"
        convDict['msg'] = "token is invalid!"
        convList["failed"] = convDict
        return convList
    
    UUID = decode.get("UUID")
    userID = decode.get("userID")

    convDict['userID'] = userID
    convDict['UUID'] = UUID

    convList['userData'] = convDict
    return convList
