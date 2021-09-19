import os

from flask import Flask
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

app.register_blueprint(addNewReserve.front)
app.register_blueprint(getReserveData.front)

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

from login.loginVerify import tokenVerify
@app.route('/')
@tokenVerify
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
