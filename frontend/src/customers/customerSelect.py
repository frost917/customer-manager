from flask import url_for, render_template, request, Blueprint
import json, requests

from statusCodeParse import parseStatusCode

front = Blueprint('customerSelect', __name__, url_prefix='/customers')

@front.route('', methods=['GET'])
def customerSelect():
    accessToken = request.cookies.get('accessToken')

    url = 'http://localhost:6000'
    customerUrl = url + '/customers'
    headers = {'Content-Type': 'charset=utf-8', 'Authorization': accessToken}
    req = requests.get(url=customerUrl, headers=headers)

    if req.status_code != 200:
       return parseStatusCode(req.status_code)

    data = json.loads(req.text)
    customerData = data.get('customerData')

    return render_template('select-customer.html', customerData=customerData)