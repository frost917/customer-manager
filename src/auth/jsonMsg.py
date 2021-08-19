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