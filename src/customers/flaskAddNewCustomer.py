from main import app
from flask import Flask, g, request, Response
from auth.flaskAuthVerify import tokenVerify

@app.route("/customers", method=['PUT'])
@tokenVerify
def getCustomerList():
    convDict = dict()
    convList = list()

    import postgres.databaseConnection
    database = postgres.databaseConnection.PostgresControll()
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

    result = bool(database.addNewCustomer(UUID=g.get("UUID"), customerID=customerID, name=name, phoneNumber=phoneNumber))
    if result is True:
        from json import dumps
        convDict['customerID'] = customerID
        convList['successed'] = convList
        return Response(dumps(convList), status=200, mimetype="application/json")

    else:
        return Response(status=500)