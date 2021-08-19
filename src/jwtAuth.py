from typing import List
import jwt
import secret


# return JWT
def createToken(userID, UUID):
    from datetime import datetime, timedelta
    body = dict()

    body['userID'] = userID
    body['UUID'] = UUID
    body['exp'] = datetime.now() + timedelta(hours=6)

    token = jwt.encode(body, key=secret.JWTSecret)
    return token

# return userData
def decodeToken(token):
    convDict = dict()
    convList = list()
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
