from flask import Response, make_response, redirect

from login.responseEnum import ResponseType
from datetime import datetime
from dateutil.relativedelta import relativedelta

def buildResponse(tokens: dict, responseType: ResponseType) -> Response:
    accessToken = tokens.get('accessToken')
    refreshToken = tokens.get('refreshToken')
    tokenTime = tokens.get('tokenTime')

    if responseType == ResponseType.LOGIN:
        response = make_response(redirect('/'))
        response.set_cookie('accessToken', accessToken, 
            expires=datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(hours=6), 
            secure=True, httponly=True)
        response.set_cookie('refreshToken', refreshToken, 
        expires=datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(months=6), 
        secure=True, httponly=True)
    
    elif responseType == ResponseType.LOGOUT:
        response = make_response(redirect('/login'))
        response.delete_cookie(accessToken, secure=True, httponly=True)
        response.delete_cookie(refreshToken, secure=True, httponly=True)

    elif responseType == ResponseType.TOKENEXPIRE:
        response = make_response(redirect('/login'))

    elif responseType == ResponseType.REFRESH:
        response = make_response("""<script>location.reload();</script>""")
        response.set_cookie('accessToken', accessToken, 
            expires=datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(hours=6), 
            secure=True, httponly=True)
        response.set_cookie('refreshToken', refreshToken, 
        expires=datetime.strptime(tokenTime, '%Y-%m-%d %H:%M:%S.%f') + relativedelta(months=6), 
        secure=True, httponly=True)

    elif responseType == ResponseType.ERROR:
        response = make_response("""<script>
        alert("서버 에러");
        history.back();
        </script>""")

    elif responseType == ResponseType.ACCOUNTERROR:
        response = make_response("""<script>
            alert("아이디 또는 비밀번호가 잘못되었습니다");
            location.href="/login";
            </script>""")

    return response