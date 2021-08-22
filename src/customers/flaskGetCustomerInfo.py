from main import app
from flask import Response, g, request
from auth.flaskAuthVerify import tokenVerify

@app.route("/customers/<customerID>", method=['GET'])
@tokenVerify
def getCustomerInfo():
    import postgres.databaseConnection
    database = postgres.databaseConnection.PostgresControll()
    # 데이터가 JSON이 아닐 경우 거부
    if request.is_json == False:
        from msg.jsonMsg import dataNotJSON
        return Response(dataNotJSON(), status=400)

    data = request.get_json()
    
    tmpID = data["customerID"]
    customerID = tmpID if tmpID is not None else "None"
    UUID = g["UUID"]

    result = database.getCustomerInfo(UUID=UUID, customerID=customerID)

    import json
    return Response(json.dumps(result), status=200)
