from functools import wraps

from flask import g, request

from login.responseBuilder import buildResponse
from login.responseEnum import ResponseType

# json 데이터 분해 및 별도 저장
def dataParsing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.is_json == False:
            return buildResponse(None, ResponseType.ERROR)

        try:
            data = request.get_json()
        except:
            return buildResponse(None, ResponseType.ERROR)
        # 손님 리스트
        g.customers = data.get('customerData')

        # 시술 리스트
        g.jobs = data.get('jobData')

        # 방문 기록 파싱
        # tmpVisitDate = str(data['job']['visitDate'])
        # tmpJobID = str(data['job']['jobID'])

        return func(*args, **kwargs)
    return wrapper
