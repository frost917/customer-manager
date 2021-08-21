from main import app

from flask import Flask, request, jsonify, redirect, Response
from flask.helpers import make_response

@app.route("/auth")
def login():
    userID = request.form.get('userID')
    password = request.form.get('passwd')

    # 메소드에 상관 없이 id, pw가 없으면 400 반환
    if userID is None or password is None:
        from msg.jsonMsg import dataMissingJson
        loginReturn = Response(dataMissingJson(), status=400, mimetype="application/json")
        return loginReturn

    from postgres.dataQuery import PostgresControll
    database = PostgresControll
    originPasswordTuple = database.getUserPasswd(userID=userID)

    if originPasswordTuple is None:
        # 비밀번호가 일치하지 않거나 계정이 없는경우
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(response=authFailedJson(userID=userID), status=400, mimetype="application/json")

        return loginReturn
    
    originPassword = database.getUserPasswd(userID=userID)[0]
    UUID = database.getUUID(userID=userID, passwd=password)[0]
    ## 이 위까지가 DB와의 연동 과정

    import bcrypt
    # 비밀번호 비교 / bool
    # 로그인 성공시 json으로 토큰 넘겨줌
    # 인증 토큰은 쿠키에 저장
    passComp = bcrypt.checkpw(
        password=password.encode('utf-8'),
        hashed_password=originPassword)
    if passComp:
        from auth.jwtTokenProcess import createAccessToken, createRefreshToken
        accessToken = createAccessToken(userID=userID, UUID=UUID)
        refreshToken = createRefreshToken()

        # 인증 성공시 인증 토큰 반환
        convList = list()
        convList['userID'] = userID
        convList['accessToken'] = accessToken
        convList['refreshToken'] = refreshToken

        from redisCustom import redisToken
        redisToken.setRefreshToken(refreshToken=refreshToken, userID=userID,UUID=UUID)

        loginSuccessed = jsonify(convList)

        loginReturn = make_response(Response(response=loginSuccessed, status=200, mimetype="application/json"))
        loginReturn.set_cookie('userID', userID)
        loginReturn.set_cookie('accessToken', accessToken)
        loginReturn.set_cookie('refreshToken', refreshToken)
        return loginReturn

    else:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(authFailedJson(userID=userID), status=400, mimetype="application/json")

# TODO 파일 flaskAuthRefresh.py로 분리할 것
@app.route("/auth/refresh")
def tokenRefresh():
    accessToken = request.cookies.get("accessToken")
    refreshToken = request.cookies.get("refreshToken")
    refreshResult = Response()

    # 각각 토큰이 멀쩡한지 검사함
    from auth.jwtTokenProcess import isAccessTokenValid,isAccessTokenValid, createAccessToken, createRefreshToken
    from redisCustom import redisToken
    isAccessTokenExpired = isAccessTokenValid(accessToken=accessToken)
    isRefreshTokenExpired = isAccessTokenValid(refreshToken=refreshToken)

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
        userID = redisToken.getUserID(refreshToken=refreshToken)
        UUID = redisToken.getUUID(refreshToken=refreshToken)

        accessToken = createAccessToken(userID=userID, UUID=UUID)
        cookies = make_response(Response(status=200))
        cookies.set_cookie('accessToken', accessToken)

        # 새로 생성된 토큰은 쿠키로도 전달
        refreshResult = cookies

    # refresh token만 파기된 경우
    elif isRefreshTokenExpired:
        # access token을 이용해 접속자 정보 받아옴
        refreshToken = createRefreshToken()

        from auth.jwtTokenProcess import tokenGetUserID, tokenGetUUID
        # refresh token이 파기된게 확인된 순간
        # redis에서 토큰이 삭제된다
        userID = tokenGetUserID(accessToken=accessToken)
        UUID = tokenGetUUID(accessToken=accessToken)
        redisToken.setRefreshToken(refreshToken=refreshToken, userID=userID, UUID=UUID)

        cookies = make_response(Response(status=200))
        cookies.set_cookie('refreshToken', refreshToken)
        refreshResult = cookies

    return refreshResult
