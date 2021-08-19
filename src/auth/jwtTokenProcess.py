import jwt
import secret
from datetime import datetime, timedelta

# return Access token
def createAccessToken(userID, UUID):
    body = dict()
    body['userID'] = userID
    body['UUID'] = UUID

    token = jwt.encode({"exp": datetime.now() + timedelta(hours=3)}, payload=body, key=secret.JWTSecret)
    return token

# return RefreshToken
# To save redis
def createRefreshToken():
    token = jwt.encode({"exp": datetime.now() + timedelta(hours=6)}, key=secret.JWTSecret)
    return token

# return userData
def decodeToken(token):
    convDict = dict()
    convList = list()

    # 토큰 디코딩 후 에러 발생시
    # 해당 에러에 대응되는 JSON 객체 반환
    try:
        decode = jwt.decode(token, secret.getJWTSecret())
    except jwt.ExpiredSignatureError as ERR:
        convDict['error'] = "TokenExpired"
        convDict['msg'] = "token is expired!"
        convList["failed"] = convDict
        return convList
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
