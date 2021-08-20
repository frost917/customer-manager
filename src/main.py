from flask import Flask, request, jsonify, redirect, Response
from flask.helpers import make_response
from flask.templating import render_template
import os

app = Flask(__name__)
app.secret_key = os.urandom(20)

# JSON 한글 깨짐 방지를 위해
app.config['JSON_AS_ASCII'] = False
app.config['SERVER_NAME'] = "0.0.0.0:5000"
# @app.route("/install")
# def install():
#     db = postgresAttach.connect().cursor()
#     s

# TODO 이거 다 쪼개서 파일 나눌것

# 굳이 필요는 없지만 그냥 한번 만들어봄
@app.route("/", method=['GET', 'POST'])
def index():
    try:
        token = request.headers.get('token')
    except:
        from msg.jsonMsg import dataMissingJson
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

# @app.route('/visit-history')

if __name__ == "__main__":
    pass