from typing import Literal
from flask import make_response, redirect
import requests
import json

def parseStatusCode(req: requests.Response) -> Literal:
    if req.status_code == 400:
        errMsg: str = json.loads(req.text).get('failed').get('error')
        if errMsg == 'AuthFailed':
            retMsg =  """<script>
        alert("아이디 또는 비밀번호가 잘못되었습니다");
        history.back();
        </script>"""
        elif errMsg == 'MissingData':
            retMsg = """<script>
        alert("일부 데이터가 누락되었습니다.");
        history.back();
        </script>"""
        else:
            retMsg = """<script>
            alert("데이터가 잘못되었습니다");
            history.back();
            </script>"""

        return retMsg

    elif req.status_code == 401:
        result = make_response(redirect('/login'))
        result.delete_cookie('accessToken')
        result.delete_cookie('refreshToken')
        result.delete_cookie('tokenTime')
        return result

    elif req.status_code == 404:
        return """<script>
        alert("해당 데이터가 없습니다.");
        history.back();
        </script>"""
    elif 500 <= req.status_code and req.status_code <= 599:
        return """<script>
        alert("서버 에러");
        history.back();
        </script>"""