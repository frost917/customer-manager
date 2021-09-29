from typing import Literal
from datetime import datetime
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
        accessToken = tokenData.get('accessToken')
        refreshToken = tokenData.get('refreshToken')
        tokenTime = tokenData.get('tokenTime')
        expireTime = int(
            datetime.strptime(tokenData.get('expireTime'), '%Y-%m-%d %H:%M:%S.%f').timestamp())

        tokenParsed = { 'accessToken': accessToken,
        'refreshToken': refreshToken,
        'tokenTime': tokenTime,
        'expireTime': expireTime
        }
        
        return tokenParsed

    # refreshToken이 만료된 경우
    elif req.status_code == 401:
        return False

    else:
        return parseStatusCode(req)
