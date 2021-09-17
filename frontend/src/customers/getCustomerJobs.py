from flask import url_for, render_template, request, Blueprint
import json, requests

from statusCodeParse import parseStatusCode

front = Blueprint('customerJobData', __name__, url_prefix='/customers')

@front.route('/<customerID>', methods=['GET'])
def customerJobData(customerID):
    accessToken = request.cookies.get('accessToken')

    url = 'http://localhost:6000'
    customerUrl = url + '/jobs/customer/' + customerID
    headers = {'Content-Type': 'charset=utf-8', 'Authorization': accessToken}
    req = requests.get(url=customerUrl, headers=headers)

    if req.status_code != 200:
       return parseStatusCode(req.status_code)

    data = json.loads(req.text)
    customerData = data.get('customerData')
    jobData = data.get('jobData')

    return render_template('customer-data.html', customerData=customerData, jobData=jobData)