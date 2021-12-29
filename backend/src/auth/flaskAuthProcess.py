from datetime import datetime
from flask import Response, request, Blueprint
import json

manager = Blueprint("auth", __name__, url_prefix='/auth')

#TODO 여기 코드 정리할 것
@manager.route('', methods=['POST'])
def login():
    ## 받은 데이터 검증 단계
    if request.is_json == False:
        from msg.jsonMsg import dataNotJSON
        return Response(dataNotJSON(), status=400, content_type="application/json; charset=UTF-8")

    try:
        data = request.get_json()
    except:
        print(request.data.decode('utf-8'))
        from msg.jsonMsg import dataMissingJson
        return Response(dataMissingJson(), status=400, content_type="application/json; charset=UTF-8")

    ## 받은 데이터의 무결성 확인
    userID: str = data['userID']
    passwd: str = data['passwd']

    # 메소드에 상관 없이 id, pw가 없으면 400 반환
    if userID is None or passwd is None:
        from msg.jsonMsg import dataMissingJson
        return Response(dataMissingJson(), status=400, content_type="application/json; charset=UTF-8")

    ## 받은 데이터의 대한 검증 
    from postgres.databaseConnection import PostgresControll
    database = PostgresControll()

    originPasswordDict = database.getUserPasswd(userID=userID)

    # db가 죽은 경우
    if originPasswordDict is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, content_type="application/json; charset=UTF-8")

    originPassword = originPasswordDict.get("passwd")

    ## 전달받은 계정의 존재 유무 확인
    # 쿼리한 비밀번호 값이 없을 경우 로그인 실패
    if originPassword is None:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(authFailedJson(userID=userID), status=400, content_type="application/json; charset=UTF-8")
    else:
        # 비밀번호 값이 존재할 경우 타입을 정확하게 하기 위함
        originPassword = str(originPassword)

    ## 계정 인증 통과 검증
    import bcrypt
    # 비밀번호 비교 / bool
    # 로그인 성공시 json으로 토큰 넘겨줌
    # 인증 토큰은 쿠키에 저장
    passComp = bcrypt.checkpw(
        password=passwd.encode('utf-8'), 
        hashed_password=originPassword.encode('utf-8')
    )
    if passComp is True:
        # 비밀번호가 맞는건 확인했으니 id로만 uuid 불러옴
        UUID = database.getUUID(userID=userID).get('user_id')

        refTime = datetime.now()

        # jwt를 생성 하는 단계
        from auth.jwtTokenProcess import createAccessToken, createRefreshToken
        accessToken = createAccessToken(
            userID=userID, 
            UUID=UUID, 
            refTime=refTime
        )
        refreshToken = createRefreshToken(
            refTime=refTime
        )
        # jwt 생성 완료

        # 인증 성공시 인증 토큰 반환
        payload = dict()
        payload['userID'] = userID
        payload['accessToken'] = accessToken
        payload['refreshToken'] = refreshToken
        # 정확한 토큰 만료 시간 표기를 위해 토큰 생성 기준 시간도 포함해 전달
        payload['tokenTime'] = refTime.strftime('%Y-%m-%d %H:%M:%S.%f')

        from redisCustom import redisToken
        redisData = redisToken()
        saveRefreshTokenResult = redisData.setRefreshToken(
            refreshToken=refreshToken, 
            userID=userID,
            UUID=UUID
        )

        # 토큰 설정에 실패한 경우(redis가 죽어서)
        if saveRefreshTokenResult == False:
            from msg.jsonMsg import redisIsGone
            loginReturn = Response(redisIsGone(), status=500, content_type="application/json; charset=UTF-8")

        loginReturn = Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")

    ## 로그인 실패
    else:
        from msg.jsonMsg import authFailedJson
        loginReturn = Response(authFailedJson(), status=400, content_type="application/json; charset=UTF-8")

    return loginReturn
