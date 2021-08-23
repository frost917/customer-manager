from functools import wraps

import jwt
from flask import Response, g, redirect, request


# 로그인 여부 확인하는 함수
def tokenVerify(func):
    @wraps(func)
    def verification(*args, **kwargs):
        accessToken = request.headers.get('Authorization')
        if accessToken is not None:
            from config.secret import JWTSecret
            try:
                decode = jwt.decode(accessToken, JWTSecret)
            except jwt.InvalidSignatureError:
                decode = None
            except jwt.ExpiredSignatureError:
                # 토큰이 파기된 경우 재발급 받으러
                return redirect("/auth/refresh")
            except jwt.InvalidTokenError:
                decode = None

            from msg.jsonMsg import authFailedJson
            if decode is None: return Response(authFailedJson(), status=401)

            # 디코딩된 값이 None라면 에러 방지를 위해 기본값 넣어줌
            userID = str(decode.get("userID"))
            UUID = str(decode.get("UUID"))

            g.userID = userID if userID is not None else ""
            g.UUID = UUID if UUID is not None else ""

        else:
            from msg.jsonMsg import dataMissingJson
            return Response(dataMissingJson(), status=400)
        
        return func(*args, **kwargs)
    return verification
