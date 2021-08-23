import os

from flask import Flask, Response, g

import auth.flaskAuthProcess
import auth.flaskAuthRefresh
import customers.flaskAddNewCustomer
import customers.flaskDeleteCustomer
import customers.flaskGetCustomerData
import customers.flaskGetCustomerList
import customers.flaskUpdateCustomerInfo
from auth.flaskAuthVerify import tokenVerify

app = Flask(__name__)
app.secret_key = os.urandom(20)

# auth
app.register_blueprint(auth.flaskAuthProcess.manager)
app.register_blueprint(auth.flaskAuthRefresh.manager)

# customers
app.register_blueprint(customers.flaskAddNewCustomer.manager)
app.register_blueprint(customers.flaskDeleteCustomer.manager)
app.register_blueprint(customers.flaskGetCustomerData.manager)
app.register_blueprint(customers.flaskGetCustomerList.manager)
app.register_blueprint(customers.flaskUpdateCustomerInfo.manager)

# TODO jsonify는 다 json.dumps로 교체할 것

# JSON 한글 깨짐 방지를 위해
app.config['JSON_AS_ASCII'] = False
# @app.route("/install")
# def install():
#     db = postgresAttach.connect().cursor()
#     s

# 굳이 필요는 없지만 그냥 한번 만들어봄
@app.route("/")
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
    app.run(host="0.0.0.0", port=5000)
