from main import app
from flask import Response, g, request
from auth.flaskAuthVerify import tokenVerify

@app.route("/customers/<customerID>", method=['PUT'])
@tokenVerify
def updateCustomerInfo():
    import postgres.databaseConnection
    database = postgres.databaseConnection.PostgresControll()
    # 데이터가 JSON이 아닐 경우 거부
    if request.is_json == False:
        from msg.jsonMsg import dataNotJSON
        return Response(dataNotJSON(), status=400)

    data = request.get_json()
    
    tmpID = data["customerID"]
    tmpName = data["name"]
    tmpPhoneNumber = data["phoneNumber"]
    customerID = tmpID if tmpID is not None else "None"
    name = tmpName if tmpName is not None else "None"
    phoneNumber = tmpPhoneNumber if tmpPhoneNumber is not None else "01000000000"
    UUID = g["UUID"]

    customerData = dict()
    customerData["customerID"] = customerID
    customerData["name"] = name
    customerData["phoneNumber"] = phoneNumber

    result = database.getCustomerInfo(UUID=UUID, customerID=customerID)

    import json
    return Response(json.dumps(result), status=200)
