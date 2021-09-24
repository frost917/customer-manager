from flask import make_response, redirect
import json

def parseStatusCode(req):
    if req.status_code == 400:
        print(json.loads(req.text))
        return """<script>
        alert("데이터가 잘못되었습니다");
        history.back();
        </script>"""
    elif req.status_code == 401:
        result = make_response(redirect('/login'))
        result.delete_cookie('accessToken')
        result.delete_cookie('refreshToken')
        return result
    elif req.status_code == 404:
        print(json.loads(req.text))
        return """<script>
        alert("해당 데이터가 없습니다.");
        history.back();
        </script>"""
    elif 500 <= req.status_code and req.status_code <= 599:
        print(json.loads(req.text))
        return """<script>
        alert("서버 에러");
        history.back();
        </script>"""