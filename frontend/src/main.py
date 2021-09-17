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

# 작업 관련 페이지 블루프린트

from jobs import addNewJob

app.register_blueprint(addNewJob.front)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
