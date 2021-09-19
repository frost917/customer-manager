from auth.flaskAuthVerify import tokenVerify
import json
from functools import wraps

from flask import Response, g, request

# json 데이터 분해 및 별도 저장
def dataParsing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('데이터 파싱 시작')
        if request.is_json == False:
            print('데이터 형식이 JSON이 아님')
            from msg.jsonMsg import dataNotJSON
            return Response(dataNotJSON(), status=400)

        try:
            data = request.get_json()
        except:
            print('데이터 파싱 실패')
            from msg.jsonMsg import dataNotJSON
            return Response(dataNotJSON(), status=400)

        # 손님 리스트
        g.customers = data.get('customerData')

        # 시술 리스트
        g.jobs = data.get('jobData')

        # 예약 리스트
        g.reserves = data.get('reserveData')
        print('데이터 파싱 성공')
        return func(*args, **kwargs)
    return wrapper
