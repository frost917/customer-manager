from flask import Response, redirect

def parseStatusCode(status_code):
    if status_code == 401:
        return """<script>
        history.go(-1);
        </script>"""
    elif 400 <= status_code and status_code <= 499:
        return """<script>
        alert("데이터가 잘못되었습니다");
        history.back();
        </script>"""
    elif 500 <= status_code and status_code <= 599:
        return """<script>
        alert("서버 에러");
        history.go(-1);
        </script>"""