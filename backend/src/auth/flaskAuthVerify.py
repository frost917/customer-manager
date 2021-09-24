from functools import wraps
from flask import Response, g, request

from auth.jwtTokenProcess import tokenGetUserID, tokenGetUUID

# 로그인 여부 확인하는 함수
def tokenVerify(func):
    @wraps(func)
    def verification(*args, **kwargs):
        accessToken = request.headers.get('Authorization')

        if accessToken is None:
            import json
            return Response(json.dumps('Unauthorized'), status=401, content_type="text/html; charset=UTF-8")

        userID = tokenGetUserID(accessToken=accessToken)
        UUID = tokenGetUUID(accessToken=accessToken)

        if type(UUID) is str and len(UUID) == 36:
            g.userID = userID
            g.UUID = UUID
        else:
            return Response(status=401)

        return func(*args, **kwargs)
    return verification
