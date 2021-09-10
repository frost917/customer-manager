import json
from functools import wraps

from flask import Response, g, request


# 로그인 여부 확인하는 함수
def dataParsing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.is_json == False:
            from msg.jsonMsg import dataNotJSON
            return Response(dataNotJSON(), status=400)

        data = dict(request.get_json())

        # 손님 정보 파싱
        g.customers = list(data.get('customerData'))        
        # tmpCustomerName = str(data.get('customerData').get('customerName'))
        # tmpPhoneNumber = str(data['customerData']['phoneNumber'])
        # tmpCustomerID = str(data['customerID'])

        # g.customerName = tmpCustomerName if tmpCustomerName is not None else ""
        # g.phoneNumber = tmpPhoneNumber if tmpPhoneNumber is not None else ""
        # g.customerID = tmpCustomerID if tmpCustomerID is not None else ""

        # 작업 기록 딕셔너리
        g.jobs = data.get('jobData')

        # 방문 기록 파싱
        # tmpVisitDate = str(data['job']['visitDate'])
        # tmpJobID = str(data['job']['jobID'])

        # g.visitDate = tmpVisitDate if tmpVisitDate is not None else ""
        # g.jobID = tmpJobID if tmpJobID is not None else ""

        # # 작업 관련 파싱
        # tmpPrice = float(data['job']['price'])
        # tmpJobsFinished = list(data['job']['jobsFinished'])
        # tmpJobDescription = str(data['job']['jobDescription'])

        # g.price = int(tmpPrice) if int(tmpPrice) is not None else 0
        # g.jobsFinished = list(tmpJobsFinished) if list(tmpJobsFinished) is not None else list()
        # g.jobDescription = str(tmpJobDescription) if str(tmpJobDescription) is not None else ""
        
        return func(*args, **kwargs)
    return wrapper
