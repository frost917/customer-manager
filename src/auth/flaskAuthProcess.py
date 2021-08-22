from main import app

from flask import Flask, request,  redirect, Response
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

    from postgres.databaseConnection import PostgresControll
    database = PostgresControll()
    originPasswordTuple = database.getUserPasswd(userID=userID)
    UUIDTuple = database.getUUID(userID=userID, passwd=password)[0]

    # db가 죽은 경우
    if originPasswordTuple is None or UUIDTuple is None:
        loginReturn = Response(status=500, mimetype="application/json")

        return loginReturn

    # 튜플 길이가 둘 다 0인 경우
    # 해당 데이터가 없는 것으로 판단
    elif len(originPasswordTuple) * len(UUIDTuple) == 0:
        # 비밀번호가 일치하지 않거나 계정이 없는경우
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(response=authFailedJson(userID=userID), status=400, mimetype="application/json")

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
        redisData = redisToken()
        result = redisData.setRefreshToken(refreshToken=refreshToken, userID=userID,UUID=UUID)

        # 토큰 설정에 실패한 경우(redis가 죽어서)
        if result == False:
            loginReturn = Response(status=500)

        import json
        loginSuccessed = json.dumps(convList)

        loginReturn = make_response(Response(response=loginSuccessed, status=200, mimetype="application/json"))
        loginReturn.set_cookie('userID', userID)
        loginReturn.set_cookie('accessToken', accessToken)
        loginReturn.set_cookie('refreshToken', refreshToken)

    else:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(authFailedJson(), status=400, mimetype="application/json")

    return loginReturn