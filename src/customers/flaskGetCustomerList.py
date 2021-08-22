from main import app
from flask import Flask, request, g, jsonify, redirect, Response
from auth.flaskAuthVerify import tokenVerify
from json import dumps

@app.route("/customers", method=['GET'])
@tokenVerify
def getCustomerList():
    import postgres.databaseConnection
    database = postgres.databaseConnection.PostgresControll()

    # UUID를 이용해 고객 명단 불러옴
    customerTuple = tuple(database.getCustomerTuple(UUID=g.get("UUID")))

    # DB 에러인 경우에만 None 반환하므로
    # None인 경우 DB에러로 간주
    if customerTuple is None:
        from msg.jsonMsg import databaseQeuryFailed
        result = Response(databaseQeuryFailed(), status=500,mimetype="application/json")
    else:
        result = Response(dumps(customerTuple), status=200, mimetype="application/json")

    return result