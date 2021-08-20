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

@app.route("/auth/refresh")
def tokenRefresh():
    accessToken = request.cookies.get("accessToken")
    refreshToken = request.cookies.get("refreshToken")
    refreshResult = Response()

    from auth.jwtTokenProcess import isTokenValid, createAccessToken, createRefreshToken
    from redisCustom import redisToken
    result = isTokenValid(accessToken=accessToken, refreshToken=refreshToken)
    if result is None:
        refreshResult = Response(status=401)

    elif result["accessTokenExpired"] and result["refreshTokenExpired"]:
        refreshResult = Response(status=401)

    elif result["accessTokenExpired"]:
        # access token이 파기된 경우
        # redis에서 refresh token을 이용해
        # 정보를 받아와서 새 access token을 전달
        userID = redisToken.getUserID(refreshToken=refreshToken)
        UUID = redisToken.getUUID(refreshToken=refreshToken)

        accessToken = createAccessToken(userID=userID, UUID=UUID)
        cookies = make_response(Response(status=200))
        cookies.set_cookie('accessToken', accessToken)

        refreshResult = cookies

    elif result["refreshTokenExpired"]:
        # access token을 이용해 접속자 정보 받아옴
        from jwtTokenProcess import decodeToken
        refreshToken = createRefreshToken()
        userData = decodeToken(accessToken)

        userID = userData['userID']
        UUID = userData['UUID']
        redisToken.setRefreshToken(refreshToken=refreshToken, userID=userID, UUID=UUID)

        cookies = make_response(Response(status=200))
        cookies.set_cookie('refreshToken', refreshToken)
        refreshResult = cookies

    return refreshResult
