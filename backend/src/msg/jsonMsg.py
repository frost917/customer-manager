import json
from datetime import datetime
# Dict in List
def authFailedJson():
    payload = dict()
    convDict = dict()
    convList = list()

    convDict['error'] = "AuthFailed"
    convDict['msg'] = "Authentication Failed!"
    convList.append(convDict)

    payload['failed'] = convList

    return str(json.dumps(payload))

def dataMissingJson():
    payload = dict()
    convDict = dict()
    convList = list()

    convDict['error'] = "MissingData"
    convDict['msg'] = "some data is missing!"
    convList.append(convDict)

    payload['failed'] = convList

    return str(json.dumps(payload))

def customerNotFound(customerID):
    convDict = dict()
    convDict['error'] = 'CustomerNotFound'
    convDict['msg'] = 'customer is not found!'
    convDict['customerID'] = customerID
    
    convList = list()
    convList.append(convDict)

    payload = dict()
    payload['failed'] = convList

def jobNotFound(jobID):
    convDict = dict()
    convDict['error'] = 'jobNotFound'
    convDict['msg'] = 'job is not found!'
    convDict['jobID'] = jobID
    
    convList = list()
    convList.append(convDict)

    payload = dict()
    payload['failed'] = convList

def dataNotJSON():
    payload = dict()
    convDict = dict()
    convList = list()

    convDict['error'] = "DataMustJSON"
    convDict['msg'] = "data must be JSON object!"
    convList.append(convDict)

    payload['failed'] = convList

    return str(json.dumps(payload))

def tokenInvalid():
    payload = dict()
    convDict = dict()
    convList = list()

    convDict['error'] = "TokenInvalid"
    convDict['msg'] = "token is invalid!"
    convList.append(convDict)

    payload['failed'] = convList

    return json.dumps(payload)

def databaseIsGone():
    payload = dict()
    convDict = dict()
    convList = list()

    convDict['error'] = "DatabaseIsGone"
    convDict['msg'] = "database is dead!"
    convDict['queryDate'] = datetime.now().strftime('%Y-%m-%d')
    convList.append(convDict)

    payload['failed'] = convList

    return json.dumps(payload)

def queryingResult(data: dict):
    payload = dict()