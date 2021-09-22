import json

def parseStatusCode(req):
    if 400 == req.status_code:
        print(json.loads(req.text))
        return """<script>
        alert("데이터가 잘못되었습니다");
        history.back();
        </script>"""
    elif 404 == req.status_code:
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