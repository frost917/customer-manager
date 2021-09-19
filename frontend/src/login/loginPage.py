from flask import request, Blueprint, redirect, render_template

import requests
import json

from werkzeug.utils import redirect

front = Blueprint('loginPage', __name__, url_prefix='/login')

# 토큰 활성화 여부를 사전에 파악해서
# 로그인 페이지에 접근하는건 둘 다 없는 경우
@front.route('', methods=['GET'])
def loginPage():
    accessToken = request.form.get('accessToken')
    refreshToken = request.form.get('refreshToken')

    if accessToken is None and refreshToken is None:
        return render_template('login.html')
    else:
        return redirect('/')