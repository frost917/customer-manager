from flask import Flask, request, jsonify, session, Response
from flask.templating import render_template
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

# JSON 한글 깨짐 방지를 위해
app.config['JSON_AS_ASCII'] = False
# @app.route("/install")
# def install():
#     db = postgresAttach.connect().cursor()
#     s

# 굳이 필요는 없지만 그냥 한번 만들어봄
@app.route("/", method=['GET', 'POST'])
def index():
    if request.method == "POST":
        # 여러번 선언될 변수는 위에 미리 선언함
        convDict = dict()

        # POST 토큰 정보가 안넘어왔으면 400 반환
        try:
            token = request.form.get('token')
        except:
            return Response(jsonify(convDict), status=400, mimetype="application/json")

        # JWT Decode 결과가 list가 아닌 경우
        # 토큰이 만료된 것으로 간주
        from jwtAuth import decodeToken
        userData = decodeToken(token=token)
        if userData != list:
            return Response(jsonify(userData), status=401, mimetype="application/json")

        userID = userData['userData']['userID']
        convDict['userID'] = userID
        convDict['msg'] = "Hello, %s".format(userID)

        helloUser = jsonify(convDict)
        return Response(helloUser, status=200,mimetype="application/json")

# jwt로 싹 갈아엎어야 함
@app.route("/auth")
def login():
    convList = list()
    convDict = dict()

    userID = request.form.get('userID')
    password = request.form.get('passwd')

    # 메소드에 상관 없이 id, pw가 없으면 400 반환
    if userID is None or password is None:
        convList['error'] = "MissingData"
        convList['msg'] = "some data is missing!"
        convDict['failed'] = convList

        loginFailed = jsonify(convDict)
        loginReturn = Response(loginFailed, status=400, mimetype="application/json")
        return loginReturn

    from postgresCustom import PostgresControll
    database = PostgresControll
    originPasswordTuple = database.getUserPasswd(userID=userID)

    # 해당 유저가 없는 경우
    if originPasswordTuple is None:
        # 비밀번호가 일치하지 않거나 계정이 없는경우
        # JSON 변환용
        # 함수 도입부에 선언했음
        convList['userID'] = userID
        convList['error'] = "NoData"
        convList['msg'] = "some data not found!"

        # 함수 도입부에 선언했음
        convDict['failed'] = convList

        loginFailed = jsonify(convDict)
        loginReturn = Response(response=loginFailed, status=400, mimetype="application/json")

        return loginReturn
    
    originPassword = database.getUserPasswd(userID=userID)[0]
    UUID = database.getUUID(userID=userID, passwd=password)[0]

    import bcrypt
    # 비밀번호 비교 / bool
    # 로그인 성공시 json으로 토큰 넘겨줌
    # 인증 토큰은 쿠키에 저장
    passComp = bcrypt.checkpw(
        password=password.encode('utf-8'),
        hashed_password=originPassword)
    if passComp:
        from jwtAuth import createToken
        token = createToken(userID=userID, UUID=UUID)

        # 인증 성공시 인증 토큰 반환
        # token을 16자리 랜덤에서 JWT로 바꿀 예정
        # 함수 도입부에 선언했음
        convList['userID'] = userID
        convList['token'] = token

        loginSuccessed = jsonify(convList)
        loginReturn = Response(response=loginSuccessed, status=200, mimetype="application/json")
        return loginReturn

    else:
        convList['userID'] = userID
        convList['error'] = "AuthFailed"
        convList['msg'] = "Authentication Failed!"

        convDict['failed'] = convList
        loginReturn = Response(jsonify(convDict), status=400, mimetype="application/json")

# 손님 명단 반환하기
@app.route("/customers", method=['GET', 'POST', 'PUT'])
def customerList():
    # 인증토큰이 전송되었는지 확인
    try:
        token = request.header.get("token")
    except:
        return Response(status=400)
        
    from jwtAuth import decodeToken
    userData = decodeToken(token=token)
    if userData in "failed":
        return Response(status=401)

    UUID = userData['userData']['UUID']

    import postgresCustom
    database = postgresCustom.PostgresControll
    if request.method == "GET":
        # UUID를 이용해 고객 명단 불러옴
        customerTuple = database.getCustomerTuple(uuid=UUID)
        return Response(jsonify(customerTuple), status=200,mimetype="application/json")

    if request.method == "PUT":
        

if __name__ == "__main__":
    pass