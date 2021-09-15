from flask import Blueprint, Response, request, make_response
import json

manager = Blueprint("refresh", __name__, url_prefix='/auth')

@manager.route("/refresh")
def tokenRefresh():
    accessToken = request.headers.get("accessToken")
    refreshToken = request.headers.get("refreshToken")

    # print("header accessToken is {}".format(accessToken))
    # print("header refreshToken is {}".format(refreshToken))

    if refreshToken is None:
        refreshResult = Response('Unauthorized', status=401)

    # 각각 토큰이 멀쩡한지 검사함
    from auth.jwtTokenProcess import (createAccessToken, createRefreshToken,
                                      isAccessTokenValid, isRefreshTokenValid)
    
    isAccessTokenExpired = isAccessTokenValid(accessToken=accessToken)
    isRefreshTokenExpired = isRefreshTokenValid(refreshToken=refreshToken)

    # print('isAccessTokenExpired is {}'.format(isAccessTokenExpired))
    # print('isRefreshTokenExpired is {}'.format(isRefreshTokenExpired))

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

        # print("redis userID is {}".format(userID))
        # print("redis UUID is {}".format(UUID))

        accessToken = createAccessToken(userID=userID, UUID=UUID)
        # print("created accessToken is {}".format(accessToken))

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

    token = dict()
    token['accessToken'] = accessToken
    token['refreshToken'] = refreshToken

    # 새로 생성된 토큰은 json으로 변경해서 전달
    refreshResult = Response(json.dumps(token), status=200, mimetype='application/json') 

    return refreshResult
