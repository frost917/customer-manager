from functools import wraps

from flask import Response, g, redirect, request

from auth.jwtTokenProcess import tokenGetUserID, tokenGetUUID


# 로그인 여부 확인하는 함수
def tokenVerify(func):
    @wraps(func)
    def verification(*args, **kwargs):
        accessToken = request.headers.get('Authorization')

        if accessToken is None:
            import json
            return Response(json.dumps('Unauthorized'), status=401)

        userID = tokenGetUserID(accessToken=accessToken)
        UUID = tokenGetUUID(accessToken=accessToken)

        if type(userID) is str and type(UUID) is str:
            g.userID = userID
            g.UUID = UUID
        elif userID is Response or UUID is Response:
            return redirect('/auth/refresh')
        elif userID is None or UUID is None:
            return Response(status=401)

        print('{userID} is logined'.format(userID=userID))

        return func(*args, **kwargs)
    return verification
