from main import app
from flask import Flask, request, jsonify, redirect, Response

# 손님 명단 반환하기
@app.route("/customers", method=['GET', 'POST', 'PUT'])
def customerList():
    # 인증토큰이 전송되었는지 확인
    try:
        token = request.header.get("Authorization")
    except:
        return Response(status=400)
        
    # 토큰 전달시 
    from auth.jwtTokenProcess import decodeToken
    userData = decodeToken(token=token)
    # UUID가 None일 경우 토큰이 파기된 것으로 간주
    # refresh token을 이용한 재인증 시도
    if userData['userData']['UUID'] is None:
        return redirect("/auth/refresh", code=302)
    UUID = userData['userData']['UUID']
    convDict = dict()
    convList = list()

    import postgres.dataQuery
    database = postgres.dataQuery.PostgresControll
    # UUID를 이용해 고객 명단 불러옴
    if request.method == "GET":
        customerTuple = database.getCustomerTuple(uuid=UUID)
        return Response(jsonify(customerTuple), status=200,mimetype="application/json")

    # 새 손님 생성
    # TODO 손님 중복 체크 기능 필요함
    elif request.method == "PUT":
        # 데이터가 JSON이 아닐 경우 거부
        if request.is_json == False:
            from msg.jsonMsg import dataNotJSON
            return Response(dataNotJSON(), status=400)

        data = request.get_json()
        
        # 데이터가 없는 경우 None을 반환하므로
        # 기본값을 설정해둔다
        name = data["name"] if data["name"] is not None else "이름없음"
        phoneNumber = data["phoneNumber"] if data["phoneNumber"] is not None else "01000000000"

        import uuid
        customerID = uuid.uuid4()

        database.addNewCustomer(UUID=UUID, customerID=customerID, name=name, phoneNumber=phoneNumber)
        convDict['customerID'] = customerID

        return Response(jsonify(convList), status=200)

# TODO customerID로 접근시 데이터 불러오는 기능 추가
# @app.route('/customers/<customerID>')
