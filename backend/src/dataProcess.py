from auth.flaskAuthVerify import tokenVerify
import json
from functools import wraps

from flask import Response, g, request

# json 데이터 분해 및 별도 저장
def dataParsing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.is_json == False:
            from msg.jsonMsg import dataNotJSON
            return Response(dataNotJSON(), status=400)

        try:
            data = request.get_json()
        except:
            from msg.jsonMsg import dataNotJSON
            return Response(dataNotJSON(), status=400)

        # 손님 리스트
        g.customers = data.get('customerData')

        # 시술 리스트
        g.jobs = data.get('jobData')

        return func(*args, **kwargs)
    return wrapper
