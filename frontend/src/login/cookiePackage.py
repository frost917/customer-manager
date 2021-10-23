from flask import make_response, redirect
from datetime import timedelta

def setRefreshTokenCookie(result: make_response, tokenData: dict):
    refreshToken = tokenData.get('refreshToken')
    tokenTime = tokenData.get('tokenTime')
    expireTime = tokenData.get('expireTime')

    result.set_cookie(
        'refreshToken', refreshToken,
        max_age=expireTime, 
        httponly=True, secure=True)
    result.set_cookie(
        'tokenTime', tokenTime,
        max_age=expireTime,
        httponly=True, secure=True)

    return result

def setAccessTokenCookie(result: make_response, tokenData: dict):
    accessToken = tokenData.get('accessToken')
    result.set_cookie(
        'accessToken', accessToken, 
        max_age=timedelta(hours=3), 
        httponly=True, secure=True)

    return result

def destroyCookie():
    result = make_response(redirect('/login'))
    result.delete_cookie('accessToken')
    result.delete_cookie('refreshToken')
    result.delete_cookie('tokenTime')

    return result