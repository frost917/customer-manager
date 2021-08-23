from functools import wraps
from flask import request, g, Response

# 로그인 여부 확인하는 함수
def dataParsing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.is_json == False:
            from msg.jsonMsg import dataNotJSON
            return Response(dataNotJSON(), status=400)

        data = request.get_json()

        g.name = str(data["name"]) if str(data["name"]) is not None else ""
        g.phoneNumber = str(data["phoneNumber"]) if str(data["phoneNumber"]) is not None else ""
        g.customerID = str(data["customerID"]) if str(data["customerID"]) is not None else ""
        g.price = int(data["customerID"]) if int(data["customerID"]) is not None else 0
        
        return func(*args, **kwargs)
    return wrapper