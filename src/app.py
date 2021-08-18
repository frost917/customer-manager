from flask import Flask, session, request, jsonify
import flask
from flask.templating import render_template
import os
# import psycopg2 as sql

app = Flask(__name__)
app.secret_key = os.urandom(32)

# @app.route("/install")
# def install():
#     db = dbconn.connect().cursor()
#     s

# 굳이 필요는 없지만 그냥 한번 만들어봄
@app.route("/", method=['GET', 'POST'])
def index():
    if request.method == "POST":
        # POST 토큰 정보가 안넘어왔으면 400 반환
        try:
            token = request.form.get('token')
        except:
            convDict = dict()
            return flask.Response(convDict, status=400)

        # 토큰이 redis에 저장되어 있는 경우 한정
        try:
            from redis import StrictRedis, RedisError
            redisConn = StrictRedis(
                os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                db=0)
            userID = redisConn.hget(token, "userID")

            convDict = dict()
            convDict['userID'] = userID
            convDict['msg'] = "Hello, %s".format(userID)

            helloUser = flask.jsonify(convDict)
            return flask.Response(helloUser, status=200)
        except RedisError() as err:
            print(err)
            return flask.Response(status=500)


@app.route("/login", method=['GET', 'POST'])
def login():
    import dbconn

    # GET Method 로 들어온 경우 400 에러 반환
    loginReturn = flask.Response(status=400)

    if request.method == "POST":
        try:
            userID = request.form.get('userID')
            password = request.form.get('passwd')
        except:
            convList = list()
            convList['error'] = "NoData"
            convList['msg'] = "some data is missing!"

            convDict = dict()
            convDict['failed'] = convList

            loginFailed = flask.jsonify(convDict)
            loginReturn = flask.Response(loginFailed,
            status=400, 
            content_type="application/json")
            return loginReturn

        database = dbconn.Database
        originPasswordTuple = database.getUserPasswd(
            userID=userID)

        # 해당 유저가 있는 경우
        if originPasswordTuple is not None:
            uuidTuple = database.getUUID(
                userID=userID, passwd=password)

            import bcrypt
            # 비밀번호 비교 / bool
            # 로그인 성공시 json으로 토큰 넘겨줌
            # 인증 토큰은 쿠키에 저장
            passComp = bcrypt.checkpw(
                password=password.encode('utf-8'),
                hashed_password=originPasswordTuple[1])
            if passComp:
                # redis 연동
                # hash로 userID:uuid 저장
                try:
                    from redis import StrictRedis, RedisError
                    import binascii
                    tokenStorage = StrictRedis(
                        os.getenv("REDIS_HOST"),
                        port=os.getenv("REDIS_PORT"),
                        db=0)
                    # 토큰은 16자리 값으로
                    token = binascii.hexlify(os.urandom(16))
                    tokenStorage.set(token, uuidTuple[2])
                    tokenStorage.hset(token, "userID", userID)
                    tokenStorage.hset(token, "UUID", uuidTuple[2])
                except RedisError() as err:
                    print(err)
                    return flask.Response(status=500)

                convList = list()
                convList['userID'] = userID
                convList['token'] = token

                loginSuccessed = jsonify(convList)
                loginReturn = flask.Response(response=loginSuccessed, 
                status=200, 
                content_type="application/json")

    # 비밀번호가 일치하지 않거나 계정이 없는경우
    # JSON 변환용
        convList = list()
        convList['userID'] = userID
        convList['error'] = "NoUser"
        convList['msg'] = "user not found!"

        convDict = dict()
        convDict['failed'] = convList

        loginFailed = jsonify(convDict)
        loginReturn = flask.Response(response=loginFailed, 
        status=400, 
        content_type="application/json")

    return loginReturn

# 손님 명단 추출
# @app.route("/customer/<UUID>", method=['POST'])
# def customerList():
    

# if __name__ == "__main__":