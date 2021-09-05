from flask import Response, request, Blueprint
from flask.helpers import make_response

manager = Blueprint("auth", __name__, url_prefix='/auth')

@manager.route("", methods=['POST'])
def login():
    if request.is_json == False:
        from msg.jsonMsg import dataNotJSON
        return Response(dataNotJSON(), status=400, mimetype="application/json")

    data = request.get_json()

    userID = str(data['userID'])
    passwd = str(data['passwd'])

    # 메소드에 상관 없이 id, pw가 없으면 400 반환
    if userID is None or passwd is None:
        from msg.jsonMsg import dataMissingJson
        return Response(dataMissingJson(), status=400, mimetype="application/json")

    from postgres.databaseConnection import PostgresControll
    database = PostgresControll()

    originPasswordDict = database.getUserPasswd(userID=userID)

    # db가 죽은 경우
    if originPasswordDict is None:
        return Response(status=500, mimetype="application/json")

    originPassword = str(originPasswordDict.get("passwd"))

    # 쿼리한 비밀번호 값이 없을 경우 로그인 실패
    if originPassword is None:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(response=authFailedJson(userID=userID), status=400, mimetype="application/json")

    import bcrypt
    # 비밀번호 비교 / bool
    # 로그인 성공시 json으로 토큰 넘겨줌
    # 인증 토큰은 쿠키에 저장
    passComp = bcrypt.checkpw(password=passwd.encode('utf-8'), hashed_password=originPassword.encode('utf-8'))
    if passComp:
        userData = dict()
        userData["userID"] = str(userID)
        userData["passwd"] = str(originPassword)

        UUID = database.getUUID(userData=userData).get('user_id')

        from auth.jwtTokenProcess import createAccessToken, createRefreshToken
        accessToken = createAccessToken(userID=userID, UUID=UUID)
        refreshToken = createRefreshToken()

        # 인증 성공시 인증 토큰 반환
        payload = dict()
        payload['userID'] = userID
        payload['accessToken'] = accessToken
        payload['refreshToken'] = refreshToken

        from redisCustom import redisToken
        redisData = redisToken()
        result = redisData.setRefreshToken(refreshToken=refreshToken, userID=userID,UUID=UUID)

        # 토큰 설정에 실패한 경우(redis가 죽어서)
        if result == False:
            loginReturn = Response(status=500)

        import json
        loginSuccessed = json.dumps(payload)

        loginReturn = make_response(Response(response=loginSuccessed, status=200, mimetype="application/json"))
        loginReturn.set_cookie('userID', userID)
        loginReturn.set_cookie('accessToken', accessToken)
        loginReturn.set_cookie('refreshToken', refreshToken)

    else:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(authFailedJson(), status=400, mimetype="application/json")

    return loginReturn
