from dataProcess import dataParsing
import json
from functools import wraps

from flask import Response, g

# 넘어온 데이터 확인
@dataParsing
def customerDataCheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 손님 데이터가 전달되지 않을 경우 에러 반환
        customers = g.get('customers')
        if customers is None:
            from msg.jsonMsg import dataMissingJson
            return Response(dataMissingJson(), status=400, mimetype='application/json')

        from postgres.databaseConnection import PostgresControll
        database = PostgresControll()

        # 손님 데이터가 db에 존재하는지 확인
        customerQueryDict = dict()
        for customer in customers:
            customerID = customer.get('customerID')
            customerQueryDict[customerID] = database.getCustomerData(customerID=customerID)

        # 손님 데이터가 db에 없는 경우 에러
        if len(customerQueryDict) == 0:
            convDict = dict()
            convDict['error'] = 'CustomerNotFound'
            convDict['msg'] = 'customer is not found!'
            
            convList = list()
            convList.append(convDict)

            payload = dict()
            payload['failed'] = convList

            return Response(json.dumps(payload), status=400, mimetype='application/json')

        return func(*args, **kwargs)
    return wrapper

@customerDataCheck
def jobDataCheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jobs = g.get('jobs')
        if jobs is None:
            from msg.jsonMsg import dataMissingJson
            return Response(dataMissingJson(), status=400, mimetype='application/json')

        from postgres.databaseConnection import PostgresControll
        database = PostgresControll()

        # 작업 기록이 db에 있는지 확인
        jobQueryDict = dict()
        for job in jobs:
            jobID = job.get('jobID')
            jobQueryDict[jobID] = database.getJobHistory(jobID=jobID)

        # 단 하나도 없으면 에러
        if len(jobQueryDict) == 0:
            convDict = dict()
            convDict['error'] = 'CustomerNotFound'
            convDict['msg'] = 'customer is not found!'
            
            convList = list()
            convList.append(convDict)

            payload = dict()
            payload['failed'] = convList

            return Response(json.dumps(payload), status=400, mimetype='application/json')
        return func(*args, **kwargs)
    return wrapper