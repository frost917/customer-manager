import json

def authFailedJson(userID):
    convList = list()
    convDict = dict()

    convList['userID'] = userID
    convList['error'] = "AuthFailed"
    convList['msg'] = "Authentication Failed!"

    convDict['failed'] = convList

    body = json.dump(convDict)
    return body

def dataMissingJson():
    convList = list()
    convDict = dict()

    convList['error'] = "MissingData"
    convList['msg'] = "some data is missing!"
    convDict['failed'] = convList

    body = json.dump(convDict)
    return body

def dataNotJSON():
    convList = list()
    convDict = dict()

    convDict['error'] = "DataMustJSON"
    convDict['msg'] = "data must be JSON object!"
    convList['failed'] = convDict

    body = json.dump(convDict)
    return body