import json
# Dict in List
def authFailedJson():
    payload = dict()
    convDict = dict()

    convDict['error'] = "AuthFailed"
    convDict['msg'] = "Authentication Failed!"

    payload['failed'] = convDict

    return json.dumps(payload)

def dataMissingJson():
    payload = dict()
    convDict = dict()

    convDict['error'] = "MissingData"
    convDict['msg'] = "some data is missing!"

    payload['failed'] = convDict

    return json.dumps(payload)

def dataNotJSON():
    payload = dict()
    convDict = dict()

    convDict['error'] = "DataMustJSON"
    convDict['msg'] = "data must be JSON object!"

    payload['failed'] = convDict

    return json.dumps(payload)

def tokenInvalid():
    payload = dict()
    convDict = dict()

    convDict['error'] = "TokenInvalid"
    convDict['msg'] = "token is invalid!"

    payload['failed'] = convDict

    return json.dumps(payload)

def databaseIsGone():
    payload = dict()
    convDict = dict()

    convDict['error'] = "DatabaseIsGone"
    convDict['msg'] = "database is dead!"

    payload['failed'] = convDict

    return json.dumps(payload)
