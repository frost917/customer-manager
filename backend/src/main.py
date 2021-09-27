import os

from flask import Flask, Response, g
app = Flask(__name__)
app.secret_key = os.urandom(20)

# auth
import auth.flaskAuthProcess
import auth.flaskAuthRefresh

app.register_blueprint(auth.flaskAuthProcess.manager)
app.register_blueprint(auth.flaskAuthRefresh.manager)

# customers
import customers.flaskAddNewCustomer
import customers.flaskDeleteCustomer
import customers.flaskGetCustomerData
import customers.flaskGetAllCustomer
import customers.flaskUpdateCustomerInfo

app.register_blueprint(customers.flaskAddNewCustomer.manager)
app.register_blueprint(customers.flaskDeleteCustomer.manager)
app.register_blueprint(customers.flaskGetCustomerData.manager)
app.register_blueprint(customers.flaskGetAllCustomer.manager)
app.register_blueprint(customers.flaskUpdateCustomerInfo.manager)

# jobs
import jobs.flaskAddJobHistory
import jobs.flaskGetAllJobHistory
import jobs.flaskGetJobHistory
import jobs.flaskGetSpecJobHistory

app.register_blueprint(jobs.flaskAddJobHistory.manager)
app.register_blueprint(jobs.flaskGetAllJobHistory.manager)
app.register_blueprint(jobs.flaskGetJobHistory.manager)
app.register_blueprint(jobs.flaskGetSpecJobHistory.manager)

# visit-history
import visitHistory.flaskGetAllVisitHistory
import visitHistory.flaskGetVisitHistory

app.register_blueprint(visitHistory.flaskGetAllVisitHistory.manager)
app.register_blueprint(visitHistory.flaskGetVisitHistory.manager)

# reserve
import reserve.flaskAddNewReserve
import reserve.flaskDeleteReserve
import reserve.flaskGetAllReserve
import reserve.flaskGetReserveData
import reserve.flaskGetReserveSpec
import reserve.flaskUpdateReserveData

app.register_blueprint(reserve.flaskAddNewReserve.manager)
app.register_blueprint(reserve.flaskDeleteReserve.manager)
app.register_blueprint(reserve.flaskGetAllReserve.manager)
app.register_blueprint(reserve.flaskGetReserveData.manager)
app.register_blueprint(reserve.flaskGetReserveSpec.manager)
app.register_blueprint(reserve.flaskUpdateReserveData.manager)

# 파드 생존 확인을 위한 라우팅
import liveness
app.register_blueprint(liveness.manager)

# JSON 한글 깨짐 방지를 위해
app.config['JSON_AS_ASCII'] = False

from auth.flaskAuthVerify import tokenVerify

# 굳이 필요는 없지만 그냥 한번 만들어봄
@app.route("/")
@tokenVerify
def index():
    userID = g.get('userID')
    convDict = dict()
    convDict['userID'] = userID
    convDict['msg'] = "Hello, {userID}".format(userID=userID)

    from json import dumps
    helloUser = dumps(convDict)
    return Response(helloUser, status=200, mimetype="application/json")
    
import ssl
if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(certfile='/certs/tls.crt', keyfile='/certs/tls.key')
    app.run(host="0.0.0.0", port=443, ssl_context=ssl_context)  