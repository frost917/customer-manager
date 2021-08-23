from flask import Flask, g, Response
import os
from auth.flaskAuthVerify import tokenVerify

app = Flask(__name__)
app.secret_key = os.urandom(20)

# TODO jsonify는 다 json.dumps로 교체할 것

# JSON 한글 깨짐 방지를 위해
app.config['JSON_AS_ASCII'] = False
app.config['SERVER_NAME'] = "0.0.0.0:5000"
# @app.route("/install")
# def install():
#     db = postgresAttach.connect().cursor()
#     s

# 굳이 필요는 없지만 그냥 한번 만들어봄
@app.route("/", method=['GET', 'POST'])
@tokenVerify
def index():
    userID = g.get("userID")

    convDict = dict()
    convDict['userID'] = userID
    convDict['msg'] = "Hello, %s".format(userID)

    from json import dumps
    helloUser = dumps(convDict)
    return Response(helloUser, status=200, mimetype="application/json")

# @app.route('/visit-history')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0:5000')