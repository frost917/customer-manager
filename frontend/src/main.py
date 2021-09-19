import os

from flask import Flask, g
from flask.templating import render_template
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

app.register_blueprint(customerSelect.front)
app.register_blueprint(getCustomerJobs.front)

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

import requests
import json

from login.loginVerify import tokenVerify
from config.secret import backendData
from statusCodeParse import parseStatusCode
@app.route('/')
@tokenVerify
def index():
    accessToken = g.get('accessToken')

    url = backendData['ADDR']
    reserveUrl = url + '/reserves'
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    reserveReq = requests.get(url=reserveUrl, headers=headers)

    if reserveReq.status_code != 200:
        return parseStatusCode(reserveReq.status_code)

    reserveData = json.loads(reserveReq.text).get('reserveData')
    print(reserveData)

    return render_template('index.html', reserveData=reserveData)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
