from flask import render_template, g, Blueprint

import json, requests

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from returnResponse import makeResponse
from config.backendData import backendData

front = Blueprint('customerSelect', __name__, url_prefix='/customers')
@front.route('', methods=['GET'])
@tokenVerify
@makeResponse
def customerSelect():
    accessToken = g.get('accessToken')

    url = backendData['ADDR']
    customerUrl = url + '/customers'
    headers = {'Content-Type': 'charset=utf-8', 'Authorization': accessToken}
    req = requests.get(url=customerUrl, headers=headers, verify=False)

    if req.status_code != 200:
       return parseStatusCode(req)

    data = json.loads(req.text)
    customerData = data.get('customerData')

    result = render_template('select-customer.html', customerData=customerData)
    return result