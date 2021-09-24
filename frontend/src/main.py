import os

from flask import Flask, request, render_template
app = Flask(__name__)
app.secret_key = os.urandom(20)

# 로그인 페이지 블루프린트

from login import login
from login import loginPage

app.register_blueprint(login.front)
app.register_blueprint(loginPage.front)

# 손님 페이지 블루프린트

from customers import customerSelect
from customers import getCustomerJobs
from customers import addNewCustomer

app.register_blueprint(customerSelect.front)
app.register_blueprint(getCustomerJobs.front)
app.register_blueprint(addNewCustomer.front)

# 시술 관련 페이지 블루프린트

from jobs import addNewJob
from jobs import getJobData

app.register_blueprint(addNewJob.front)
app.register_blueprint(getJobData.front)

# 예약 관련 페이지 블루프린트

from reserve import addNewReserve
from reserve import getReserveData
from reserve import updateReserveData

app.register_blueprint(addNewReserve.front)
app.register_blueprint(getReserveData.front)
app.register_blueprint(updateReserveData.front)

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

import requests, json

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

@app.route('/')
@tokenVerify
def index():
    #TODO response 생성에 사용되는 변수에서 뭔가 문제가 있는듯
    accessToken = request.cookies.get('accessToken')

    url = backendData['ADDR']
    reserveUrl = url + '/reserves'
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    reserveReq = requests.get(url=reserveUrl, headers=headers, verify=backendData['CA_CERT'])

    if reserveReq.status_code != 200:
        return parseStatusCode(req=reserveReq)

    reserveData = json.loads(reserveReq.text).get('reserveData')

    result = render_template('index.html', reserveData=reserveData)
    return result

import ssl
if __name__ == "__main__":
    if os.getenv("DEBUG") == 'True':
        app.debug = True
        app.run(host="0.0.0.0", port=5000)  
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(certfile='/customer-manager/cert/tls.crt', keyfile='/customer-manager/cert/tls.key')
        app.run(host="0.0.0.0", port=443, ssl_context=ssl_context)