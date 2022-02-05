from flask import Blueprint, render_template, request
import json
import requests
from frontend.src.login.responseBuilder import buildResponse
from frontend.src.login.responseEnum import ResponseType

from statusCodeParse import parseStatusCode
from login.loginVerify import tokenVerify
from config.backendData import backendData

front = Blueprint('getJobData', __name__, url_prefix='/jobs')
@front.route('/<jobID>', methods=['GET'])
@tokenVerify
def getJobData(jobID):
    accessToken = request.cookies.get('accessToken')

    url = backendData['ADDR'] + '/jobs/' + jobID
    headers = {'content-type': 'charset=UTF-8', 'Authorization': accessToken}
    req = requests.get(url=url, headers=headers, verify=backendData['CA_CERT'])

    if req.status_code != 200:
        responseType = ResponseType.ERROR

    data = json.loads(req.text)

    responseType    = ResponseType.GETJOBS
    customerData    = data.get('customerData')[0]
    customerID      = customerData.get('customerID')
    jobData         = data.get('jobData')

    return buildResponse(responseType, customerData=customerData, customerID=customerID, jobData=jobData)