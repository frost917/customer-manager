import requests, json

from config.backendData import backendData
from statusCodeParse import parseStatusCode

def getAccessToken(accessToken, refreshToken):
    refreshUrl = backendData['ADDR'] + '/auth/refresh'
    headers = {'accessToken': accessToken, 'refreshToken': refreshToken}
    req = requests.get(url=refreshUrl, headers=headers, verify=backendData['CA_CERT'])

    if req.status_code != 200:
        return parseStatusCode(req)

    loginData = json.loads(req.text)
    accessToken = loginData.get('accessToken')

    return accessToken

def getRefreshToken(accessToken, refreshToken):
    refreshUrl = backendData['ADDR'] + '/auth/refresh'
    headers = {'accessToken': accessToken, 'refreshToken': refreshToken}
    req = requests.get(url=refreshUrl, headers=headers, verify=backendData['CA_CERT'])

    if req.status_code != 200:
        return parseStatusCode(req)

    loginData = json.loads(req.text)
    refreshToken = loginData.get('refreshToken')

    return refreshToken
