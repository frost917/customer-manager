from flask import Flask, Blueprint, request, g, Response
from dataProcess import dataParsing
from json import dumps 
from datetime import datetime
manager = Blueprint("getAllVisitHistory", __name__, url_prefix='/visit-history')

@manager.route('/<customerID>', methods=['GET'])
@dataParsing
def getAllVisitHistory(customerID):
    from postgres.databaseConnection import PostgresControll
    database = PostgresControll()

    result = database.getVisitHistory(customerID=customerID)
    if result is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype='application/json')

    else:
        payload = dict()
        convList = list()
        payload['UUID'] = g['UUID']
        payload['queryDate'] = datetime.now()
        convList.append(result)
        payload['data'] = convList
        return Response(dumps(payload), status=200, mimetype='application/json')