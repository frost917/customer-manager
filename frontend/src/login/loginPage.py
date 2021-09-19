
from datetime import timedelta
from flask import request, Blueprint, g
from flask.helpers import make_response
from flask.templating import render_template

import requests
import json

from login.loginVerify import tokenVerify

front = Blueprint('loginPage', __name__, url_prefix='/login')

# 토큰 활성화 여부를 사전에 파악해서
# 로그인 페이지에 접근하는건 둘 다 없는 경우
@front.route('', methods=['GET'])
@tokenVerify
def loginPage():
    return render_template('login.html')