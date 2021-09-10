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
        customerQuery = database.getCustomerData(customerID=customers.get('customerID'))

        if len(customerQuery) == 0:
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
        jobQuery = database.getJobHistory(jobs.get('jobID'))

        if len(jobQuery) == 0:
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