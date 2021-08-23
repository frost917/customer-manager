from json import dumps

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Response, g, Blueprint
from postgres.databaseConnection import PostgresControll

manager = Blueprint("getCustomerList", __name__)

@manager.route("/customers", methods=['GET'])
@tokenVerify
@dataParsing
def getCustomerList():
    # UUID를 이용해 고객 명단 불러옴
    customerDict = PostgresControll().getCustomerDict(UUID=g.get("UUID"))

    # DB 에러인 경우에만 None 반환하므로
    # None인 경우 DB에러로 간주
    if customerDict is None:
        from msg.jsonMsg import databaseIsGone
        result = Response(databaseIsGone(), status=500,mimetype="application/json")
    else:
        result = Response(dumps(customerDict), status=200, mimetype="application/json")

    return result
