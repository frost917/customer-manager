import json

def parseStatusCode(req):
    if req.status_code == 401:
        print(json.loads(req.text))
        return """<script>
        history.go(-1);
        </script>"""
    elif 400 <= req.status_code and req.status_code <= 499:
        print(json.loads(req.text))
        return """<script>
        alert("데이터가 잘못되었습니다");
        history.back();
        </script>"""
    elif 500 <= req.status_code and req.status_code <= 599:
        print(json.loads(req.text))
        return """<script>
        alert("서버 에러");
        history.go(-1);
        </script>"""