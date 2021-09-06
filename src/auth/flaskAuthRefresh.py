﻿from os import access
from flask import Blueprint, Response, make_response, request

manager = Blueprint("refresh", __name__, url_prefix='/auth')

@manager.route("/refresh")
def tokenRefresh():
    print(len(request.cookies))
    print(len(request.headers))

    if len(request.cookies) != 0:
        accessToken = request.cookies.get("accessToken")
        refreshToken = request.cookies.get("refreshToken")
    elif len(request.headers) != 0:
        accessToken = request.headers.get("accessToken")
        refreshToken = request.headers.get("refreshToken")
    else:
        from msg.jsonMsg import dataMissingJson
        Response(dataMissingJson(), status=400)

    refreshResult = Response()

    # 각각 토큰이 멀쩡한지 검사함
    from auth.jwtTokenProcess import (createAccessToken, createRefreshToken,
                                      isAccessTokenValid, isRefreshTokenValid)
    
    isAccessTokenExpired = isAccessTokenValid(accessToken=accessToken)
    isRefreshTokenExpired = isRefreshTokenValid(refreshToken=refreshToken)

    from msg.jsonMsg import tokenInvalid

    # 토큰이 잘못된 경우
    if isAccessTokenExpired is None or isRefreshTokenExpired is None:
        refreshResult = Response(tokenInvalid(), status=400)

    # 토큰이 둘 다 파기된 경우
    elif isAccessTokenExpired and isRefreshTokenExpired:
        refreshResult = Response(tokenInvalid(), status=401)

    # access token만 파기된 경우 재발급
    elif isAccessTokenExpired:
        # access token이 파기된 경우
        # redis에서 refresh token을 이용해
        # 정보를 받아와서 새 access token을 전달
        from redisCustom import redisToken
        redisData = redisToken()
        userID = redisData.getUserID(refreshToken=refreshToken)
        UUID = redisData.getUUID(refreshToken=refreshToken)

        import json
        accessToken = createAccessToken(userID=userID, UUID=UUID)
        cookies = make_response(Response(json.dumps({'accessToken': accessToken}), status=200))
        cookies.set_cookie('accessToken', accessToken)

        # 새로 생성된 토큰은 쿠키로도 전달
        refreshResult = cookies

    # refresh token만 파기된 경우
    elif isRefreshTokenExpired:
        # refresh token 삭제
        from redisCustom import redisToken
        redisData = redisToken()
        result = redisData.delRefreshToken(refreshToken=refreshToken)
        # 토큰 설정에 실패한 경우(redis가 죽어서)
        if result == False:
            refreshResult = Response(status=500)

        refreshToken = createRefreshToken()

        # access token을 이용해 접속자 정보 받아옴
        from auth.jwtTokenProcess import tokenGetUserID, tokenGetUUID

        # refresh token이 파기되었을 경우
        # 이곳에서 redis에 저장된 데이터를 처리
        userID = tokenGetUserID(accessToken=accessToken)
        UUID = tokenGetUUID(accessToken=accessToken)
        result = redisData.setRefreshToken(refreshToken=refreshToken, userID=userID, UUID=UUID)

        # 토큰 설정에 실패한 경우(redis가 죽어서)
        if result == False:
            refreshResult = Response(status=500)

        cookies = make_response(Response(status=200))
        cookies.set_cookie('refreshToken', refreshToken)
        refreshResult = cookies

    return refreshResult
