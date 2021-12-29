from dateutil.relativedelta import relativedelta
from flask import Blueprint, Response, request, make_response
from datetime import datetime
import json

manager = Blueprint("refresh", __name__, url_prefix='/auth')

@manager.route("/refresh", methods=['GET', 'POST'])
def tokenRefresh():
    accessToken = request.headers.get("accessToken")
    refreshToken = request.headers.get("refreshToken")

    # 각각 토큰이 멀쩡한지 검사함
    from auth.jwtTokenProcess import (
    createAccessToken, 
    createRefreshToken,
    isAccessTokenValid, 
    isRefreshTokenValid
    )
    isAccessTokenExpired = isAccessTokenValid(accessToken=accessToken)
    isRefreshTokenExpired = isRefreshTokenValid(refreshToken=refreshToken)

    from msg.jsonMsg import tokenInvalid
    refTime = datetime.now()


    # 토큰이 잘못된 경우
    if isAccessTokenExpired is None or isRefreshTokenExpired is None:
        return Response(tokenInvalid(), status=400)

    # 토큰이 둘 다 파기된 경우
    elif isAccessTokenExpired and isRefreshTokenExpired:
        return Response('Unauthorized', status=401, content_type="text/html; charset=UTF-8")

    # access token만 파기된 경우 재발급
    elif isAccessTokenExpired:
        # access token이 파기된 경우
        # redis에서 refresh token을 이용해
        # 정보를 받아와서 새 access token을 전달
        from redisCustom import redisToken
        redisData = redisToken()
        userID = redisData.getUserID(refreshToken=refreshToken)
        UUID = redisData.getUUID(refreshToken=refreshToken)

        # 받아온 UUID의 길이가 잘못된 경우 레디스에 토큰이 없는 것으로 판단
        if type(UUID) != str or len(UUID) != 36:
            return Response('Unauthorized', status=401, content_type="text/html; charset=UTF-8")
        elif userID == None or UUID == None:
            return Response('Unauthorized', status=401, content_type="text/html; charset=UTF-8")
       
        accessToken = createAccessToken(userID=userID, UUID=UUID, refTime=refTime)
        
    # refresh token만 파기된 경우
    elif isRefreshTokenExpired:
        # refresh token 삭제
        from redisCustom import redisToken
        redisData = redisToken()
        result = redisData.delRefreshToken(refreshToken=refreshToken)

        refreshToken = createRefreshToken(refTime=refTime)

        # access token을 이용해 접속자 정보 받아옴
        from auth.jwtTokenProcess import tokenGetUserID, tokenGetUUID

        # refresh token이 파기되었을 경우
        # 이곳에서 redis에 저장된 데이터를 처리
        userID = tokenGetUserID(accessToken=accessToken)
        UUID = tokenGetUUID(accessToken=accessToken)

        if userID == None or UUID == None:
            return Response(status=401)
        elif userID is Response or UUID is Response:
            return Response(status=401)
        else:
            redisResult = redisData.setRefreshToken(refreshToken=refreshToken, userID=userID, UUID=UUID)

        # 토큰 설정에 실패한 경우(redis가 죽어서)
        if redisResult == False:
            refreshResult = Response(status=500)

    token = dict()
    token['accessToken'] = accessToken
    token['refreshToken'] = refreshToken
    token['tokenTime'] = refTime.strftime('%Y-%m-%d %H:%M:%S.%f')
    token['expireTime'] = (refTime +  relativedelta(months=1)).strftime('%Y-%m-%d %H:%M:%S.%f')

    # 새로 생성된 토큰은 json으로 변경해서 전달
    refreshResult = Response(json.dumps(token), status=200, content_type="application/json; charset=UTF-8") 

    return refreshResult
