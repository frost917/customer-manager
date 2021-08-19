from flask import Flask, request, jsonify, redirect, Response
from flask.helpers import make_response
from flask.templating import render_template
import os

app = Flask(__name__)
app.secret_key = os.urandom(20)

# JSON 한글 깨짐 방지를 위해
app.config['JSON_AS_ASCII'] = False
# @app.route("/install")
# def install():
#     db = postgresAttach.connect().cursor()
#     s

# 굳이 필요는 없지만 그냥 한번 만들어봄
@app.route("/", method=['GET', 'POST'])
def index():
    try:
        token = request.headers.get('token')
    except:
        from auth.jsonMsg import dataMissingJson
        return Response(dataMissingJson(), status=400, mimetype="application/json")

    # JWT Decode 결과가 list가 아닌 경우
    # 토큰이 만료된 것으로 간주
    from auth.jwtTokenProcess import decodeToken
    userData = decodeToken(token=token)
    if type(userData) is not type(list):
        return Response(jsonify(userData), status=401, mimetype="application/json")

    convDict = dict()
    userID = userData['userData']['userID']
    convDict['userID'] = userID
    convDict['msg'] = "Hello, %s".format(userID)

    helloUser = jsonify(convDict)
    return Response(helloUser, status=200,mimetype="application/json")

@app.route("/auth")
def login():
    userID = request.form.get('userID')
    password = request.form.get('passwd')

    # 메소드에 상관 없이 id, pw가 없으면 400 반환
    if userID is None or password is None:
        from auth.jsonMsg import dataMissingJson
        loginReturn = Response(dataMissingJson(), status=400, mimetype="application/json")
        return loginReturn

    from postgres.dataQuery import PostgresControll
    database = PostgresControll
    originPasswordTuple = database.getUserPasswd(userID=userID)

    if originPasswordTuple is None:
        # 비밀번호가 일치하지 않거나 계정이 없는경우
        from auth.jsonMsg import authFailedJson
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
        # token을 16자리 랜덤에서 JWT로 바꿀 예정
        convList = list()
        convList['userID'] = userID
        convList['accessToken'] = accessToken
        convList['refreshToken'] = refreshToken

        from redisCustom import redisToken
        redisToken.setRefreshToken(refreshToken=refreshToken, userID=userID,UUID=UUID)

        loginSuccessed = jsonify(convList)

        loginReturn = make_response(Response(response=loginSuccessed, status=200, mimetype="application/json"))
        loginReturn.set_cookie('accessToken', accessToken)
        loginReturn.set_cookie('refreshToken', refreshToken)
        return loginReturn

    else:
        from auth.jsonMsg import authFailedJson
        loginReturn = Response(authFailedJson(userID=userID), status=400, mimetype="application/json")

@app.route("/auth/refresh")
def tokenRefresh():
    refreshToken = request.cookies.get("refreshToken")

# 손님 명단 반환하기
@app.route("/customers", method=['GET', 'POST', 'PUT'])
def customerList():
    # 인증토큰이 전송되었는지 확인
    try:
        token = request.header.get("Authorization")
    except:
        return Response(status=400)
        
    # 토큰 전달시 
    from auth.jwtTokenProcess import decodeToken
    userData = decodeToken(token=token)
    # UUID가 None일 경우 토큰이 파기된 것으로 간주
    # refresh token을 이용한 재인증 시도
    if userData['userData']['UUID'] is None:
        return redirect("/auth/refresh", code=302)
    UUID = userData['userData']['UUID']

    import postgres.dataQuery
    database = postgres.dataQuery.PostgresControll
    # UUID를 이용해 고객 명단 불러옴
    if request.method == "GET":
        customerTuple = database.getCustomerTuple(uuid=UUID)
        return Response(jsonify(customerTuple), status=200,mimetype="application/json")

    if request.method == "PUT":
        

if __name__ == "__main__":
    pass