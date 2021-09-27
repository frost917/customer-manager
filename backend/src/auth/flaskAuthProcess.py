from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Response, request, Blueprint

manager = Blueprint("auth", __name__, url_prefix='/auth')

#TODO 여기 코드 정리할 것
@manager.route('', methods=['POST'])
def login():
    if request.is_json == False:
        from msg.jsonMsg import dataNotJSON
        return Response(dataNotJSON(), status=400, content_type="application/json; charset=UTF-8")

    try:
        data = request.get_json()
    except:
        print(request.data.decode('utf-8'))
        from msg.jsonMsg import dataMissingJson
        return Response(dataMissingJson(), status=400, content_type="application/json; charset=UTF-8")

    userID = data['userID']
    passwd = data['passwd']

    # 메소드에 상관 없이 id, pw가 없으면 400 반환
    if userID is None or passwd is None:
        from msg.jsonMsg import dataMissingJson
        return Response(dataMissingJson(), status=400, content_type="application/json; charset=UTF-8")

    from postgres.databaseConnection import PostgresControll
    database = PostgresControll()

    originPasswordDict = database.getUserPasswd(userID=userID)

    # db가 죽은 경우
    if originPasswordDict is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    originPassword = str(originPasswordDict.get("passwd"))

    # 쿼리한 비밀번호 값이 없을 경우 로그인 실패
    if originPassword is None:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(authFailedJson(userID=userID), status=400, content_type="application/json; charset=UTF-8")

    import bcrypt
    # 비밀번호 비교 / bool
    # 로그인 성공시 json으로 토큰 넘겨줌
    # 인증 토큰은 쿠키에 저장
    passComp = bcrypt.checkpw(password=passwd.encode('utf-8'), hashed_password=originPassword.encode('utf-8'))
    if passComp:
        userData = dict()
        userData["userID"] = userID
        userData["passwd"] = originPassword

        UUID = database.getUUID(userData=userData).get('user_id')

        refTime = datetime.now()

        from auth.jwtTokenProcess import createAccessToken, createRefreshToken
        accessToken = createAccessToken(userID=userID, UUID=UUID, refTime=refTime)
        refreshToken = createRefreshToken(refTime=refTime)

        # 인증 성공시 인증 토큰 반환
        payload = dict()
        payload['userID'] = userID
        payload['accessToken'] = accessToken
        payload['refreshToken'] = refreshToken
        payload['tokenTime'] = refTime.strftime('%Y-%m-%d %H:%M:%S.%f')
        payload['expireTime'] = (refTime +  relativedelta(months=3)).strftime('%Y-%m-%d %H:%M:%S.%f')

        from redisCustom import redisToken
        redisData = redisToken()
        result = redisData.setRefreshToken(refreshToken=refreshToken, userID=userID,UUID=UUID)

        # 토큰 설정에 실패한 경우(redis가 죽어서)
        if result == False:
            loginReturn = Response(status=500)

        import json
        loginReturn = Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")

    else:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(authFailedJson(), status=400, content_type="application/json; charset=UTF-8")

    return loginReturn
