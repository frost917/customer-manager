from main import app

from flask import request, Response
from flask.helpers import make_response

@app.route("/auth")
def login():
    userID = request.form.get('userID')
    passwd = request.form.get('passwd')

    # 메소드에 상관 없이 id, pw가 없으면 400 반환
    if userID is None or passwd is None:
        from msg.jsonMsg import dataMissingJson
        loginReturn = Response(dataMissingJson(), status=400, mimetype="application/json")
        return loginReturn

    from postgres.databaseConnection import PostgresControll
    database = PostgresControll()

    originPasswordDict = database.getUserPasswd(userID=userID)

    # db가 죽은 경우
    if originPasswordDict is None:
        loginReturn = Response(status=500, mimetype="application/json")
        return loginReturn

    originPassword = originPasswordDict.get("passwd")

    # 쿼리한 비밀번호 값이 없을 경우 로그인 실패
    if originPassword is None:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(response=authFailedJson(userID=userID), status=400, mimetype="application/json")

    import bcrypt
    # 비밀번호 비교 / bool
    # 로그인 성공시 json으로 토큰 넘겨줌
    # 인증 토큰은 쿠키에 저장
    passComp = bcrypt.checkpw(password=passwd.encode('utf-8'), hashed_password=originPassword)
    if passComp:
        userData = dict()
        userData["user_id"] = userID
        userData["passwd"] = originPassword

        UUID = database.getUUID(userData=userData)

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