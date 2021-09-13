from dataProcess import dataParsing
import json
from functools import wraps

from flask import Response, g

# 넘어온 데이터 확인
def customerDataCheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 손님 데이터가 전달되지 않을 경우 에러 반환
        customers = g.get('customers')
        customerID = func.customerID
        from postgres.databaseConnection import PostgresControll
        database = PostgresControll()
        failed = list()

        if customerID is not None:
            result = database.getCustomerData(customerID=customerID)
            if len(result) == 0:
                failed.append(customerID)

        # 손님 데이터가 db에 존재하는지 확인
        elif customers is not None:
            for customer in customers:
                customerID = customer.get('customerID')
                result = database.getCustomerData(customerID=customerID)
                if len(result) == 0:
                    failed.append(customerID)

        # customerID가 None이고 customers가 비어있지 않은 경우
        else:
            from msg.jsonMsg import dataMissingJson
            return Response(dataMissingJson(), status=400, mimetype='application/json')

        # 손님 데이터가 db에 없는 경우 에러
        if len(failed) != 0:
            convDict = dict()
            convDict['error'] = 'CustomerNotFound'
            convDict['msg'] = 'customer is not found!'
            convDict['customerList'] = failed
            
            convList = list()
            convList.append(convDict)

            payload = dict()
            payload['failed'] = convList

            return Response(json.dumps(payload), status=404, mimetype='application/json')
        return func(*args, **kwargs)
    return wrapper

def jobDataCheck(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from postgres.databaseConnection import PostgresControll
        database = PostgresControll()

        failed = list()
        jobs = g.get('jobs')
        jobID = func.jobID
        # 작업 기록이 db에 있는지 확인
        # jobID를 인자로 받은 경우
        if jobID is not None:
            result = database.getJobHistory(jobID=jobID)
            if len(result) == 0:
                failed.append(jobID)

        # 작업 데이터를 JSON으로 받은 경우
        elif jobs is not None:
            for job in jobs:
                jobID = job.get('jobID')
                result = database.getJobHistory(jobID=jobID)
                if len(result) == 0:
                    failed.append(jobID)

        # 아무것도 아닌 경우
        else:     
            from msg.jsonMsg import dataMissingJson
            return Response(dataMissingJson(), status=400, mimetype='application/json')

        # failed가 하나라도 있으면 에러
        if len(failed) != 0:
            convDict = dict()
            convDict['error'] = 'CustomerNotFound'
            convDict['msg'] = 'customer is not found!'
            
            convList = list()
            convList.append(convDict)

            payload = dict()
            payload['failed'] = convList

            return Response(json.dumps(payload), status=404, mimetype='application/json')
        return func(*args, **kwargs)
    return wrapper