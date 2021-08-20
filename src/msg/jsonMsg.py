﻿import json
# Dict in List
def authFailedJson(userID):
    convList = list()
    convDict = dict()

    convDict['userID'] = userID
    convDict['error'] = "AuthFailed"
    convDict['msg'] = "Authentication Failed!"

    convList['failed'] = convDict

    return json.dumps(convList)

def dataMissingJson():
    convList = list()
    convDict = dict()

    convDict['error'] = "MissingData"
    convDict['msg'] = "some data is missing!"

    convList['failed'] = convDict

    return json.dumps(convList)

def dataNotJSON():
    convList = list()
    convDict = dict()

    convDict['error'] = "DataMustJSON"
    convDict['msg'] = "data must be JSON object!"

    convList['failed'] = convDict

    return json.dumps(convList)

def tokenInvalid():
    convList = list()
    convDict = dict()

    convDict['error'] = "TokenInvalid"
    convDict['msg'] = "token is invalid!"

    convList['failed'] = convDict

    return json.dumps(convList)