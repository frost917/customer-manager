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
            convDict = dict()
            return Response(jsonify(convDict), status=400, mimetype="application/json")

        # 토큰이 redis에 저장되어 있는 경우
        # userID를 전달
        import redisCustom
        userID = redisCustom.redisToken.getUserID(token)
        if userID == False:
            # 함수 도입부에 선언했음
            convDict['error'] = "TokenExpired"
            convDict['msg'] = "token is expired!"

            convList = list()
            convList["failed"] = convDict

            return Response(jsonify(convList), status=401, mimetype="application/json")

        # 함수 도입부에 선언했음
        convDict['userID'] = userID
        convDict['msg'] = "Hello, %s".format(userID)

        helloUser = jsonify(convDict)
        return Response(helloUser, status=200,mimetype="application/json")


@app.route("/login", method=['GET', 'POST'])
def login():
    import postgresCustom
    convList = list()
    convDict = dict()

    if request.method == "GET":
        convList['error'] = "MissingData"
        convList['msg'] = "some data is missing!"
        convDict['failed'] = convList

        loginFailed = jsonify(convDict)
        loginReturn = Response(loginFailed, status=400, mimetype="application/json")

        # GET Method 로 들어온 경우 400 에러 반환
        loginReturn = Response(status=400)

    elif request.method == "POST":
        try:
            userID = request.form.get('userID')
            password = request.form.get('passwd')
        except:
            # 함수 도입부에 선언했음
            convList['error'] = "MissingData"
            convList['msg'] = "some data is missing!"

            # 함수 도입부에 선언했음
            convDict['failed'] = convList

            loginFailed = jsonify(convDict)
            loginReturn = Response(loginFailed, status=400, mimetype="application/json")
            return loginReturn

        database = postgresCustom.PostgresControll
        originPasswordTuple = database.getUserPasswd(userID=userID)

        # 해당 유저가 있는 경우
        if originPasswordTuple is not None:
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
                import redisCustom
                token = redisCustom.redisToken.setToken(userID, UUID)
                if token == False:
                    loginReturn = Response(status=500)
                    return loginReturn

                # 함수 도입부에 선언했음
                convList['userID'] = userID
                convList['token'] = token

                loginSuccessed = jsonify(convList)
                loginReturn = Response(response=loginSuccessed, status=200, mimetype="application/json")

    # 비밀번호가 일치하지 않거나 계정이 없는경우
    # JSON 변환용
        # 함수 도입부에 선언했음
        convList['userID'] = userID
        convList['error'] = "NoUser"
        convList['msg'] = "user not found!"

        # 함수 도입부에 선언했음
        convDict['failed'] = convList

        loginFailed = jsonify(convDict)
        loginReturn = Response(response=loginFailed, status=400, mimetype="application/json")

    return loginReturn

# 손님 명단 반환하기
@app.route("/customers", method=['GET', 'POST', 'PUT'])
def customerList():
    import postgresCustom
    # POST로 토큰이 잘 넘어왔는지 확인
    if request.method == "GET":
        pass
    elif request.method == "POST":
        try:
            token = request.form.get("token")
        except:
            return Response(status=401)
        
        # 토큰을 이용해 userID 받아오기
        import redisCustom
        UUID = redisCustom.redisToken.getUUID(token=token)

        database = postgresCustom.PostgresControll

        # UUID를 이용해 고객 명단 불러옴
        customerTuple = database.getCustomerTuple(uuid=UUID)
        return Response(jsonify(customerTuple), status=200,mimetype="application/json")
    elif request.method == "PUT":
        

if __name__ == "__main__":
    pass