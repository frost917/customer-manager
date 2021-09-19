from datetime import timedelta
from login.loginVerify import tokenVerify
from flask import render_template, g, Blueprint
import json, requests
from flask.helpers import make_response

from statusCodeParse import parseStatusCode
from config.backendData import backendData
front = Blueprint('customerSelect', __name__, url_prefix='/customers')

@front.route('', methods=['GET'])
@tokenVerify
def customerSelect():
    accessToken = g.get('accessToken')

    url = backendData['ADDR']
    customerUrl = url + '/customers'
    headers = {'Content-Type': 'charset=utf-8', 'Authorization': accessToken}
    req = requests.get(url=customerUrl, headers=headers)

    if req.status_code != 200:
       return parseStatusCode(req.status_code)

    data = json.loads(req.text)
    customerData = data.get('customerData')

    result = make_response(render_template('select-customer.html', customerData=customerData))
    result.set_cookie('accessToken', accessToken, max_age=timedelta(hours=3), httponly=True)
    return result