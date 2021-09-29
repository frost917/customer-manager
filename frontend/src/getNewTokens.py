from typing import Literal
from statusCodeParse import parseStatusCode
import requests, json

from config.backendData import backendData

refreshUrl = backendData['ADDR'] + '/auth/refresh'

def tokenRefreshing(accessToken: str, refreshToken: str):
    headers = {'accessToken': accessToken, 'refreshToken': refreshToken}
    req = requests.get(url=refreshUrl, headers=headers, verify=backendData['CA_CERT'])

    # http 코드에 따라 결과 변동

    # 어처피 accessToken, refreshToken 둘 다
    # 전송하는데 그냥 한번에 불러옴
    if req.status_code == 200:
        tokenData = json.loads(req.text)
        return tokenData

    # refreshToken이 만료된 경우
    elif req.status_code == 401:
        return False

    else:
        return parseStatusCode(req)

# def getRefreshToken(accessToken, refreshToken):
#     headers = {'accessToken': accessToken, 'refreshToken': refreshToken}
#     req = requests.get(url=refreshUrl, headers=headers, verify=backendData['CA_CERT'])

#     # http 코드에 따라 결과 변동
#     if req.status_code == 200:
#         loginData = json.loads(req.text)
#         tokenData = { 
#             'refreshToken': loginData.get('refreshToken'),
#             'tokenTime': loginData.get('tokenTime'),
#             'expireTime': loginData.get('expireTime') 
#         }
#         return tokenData

#     # refreshToken이 만료된 경우
#     elif req.status_code == 401:
#         return False

#     else:
#         return parseStatusCode(req)
