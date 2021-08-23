from functools import wraps

from flask import Response, g, request


# 로그인 여부 확인하는 함수
def dataParsing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.is_json == False:
            from msg.jsonMsg import dataNotJSON
            return Response(dataNotJSON(), status=400)

        data = request.get_json()

        # 손님 정보 파싱
        tmpName = data.get("info").get("name")
        tmpPhoneNumber = data.get("info").get("phoneNumber")
        tmpCustomerID = data.get("customerID")

        # 작업 관련 파싱
        tmpPrice = data.get("job").get("price")

        g.name = str(tmpName) if str(tmpName) is not None else ""
        g.phoneNumber = str(tmpPhoneNumber) if str(tmpPhoneNumber) is not None else ""
        g.customerID = str(tmpCustomerID) if str(tmpCustomerID) is not None else ""

        g.price = int(tmpPrice) if int(tmpPrice) is not None else 0
        
        return func(*args, **kwargs)
    return wrapper
