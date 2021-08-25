from flask import Blueprint, request, g, Response
from dataProcess import dataParsing
from auth.flaskAuthVerify import tokenVerify
from json import dumps 
from datetime import datetime
import uuid

manager = Blueprint("addNewVisitHistory", __name__)

@manager.route('/visit-history', methods=['POST'])
@tokenVerify
@dataParsing
def addNewVisitHistory():
    from postgres.databaseConnection import PostgresControll
    database = PostgresControll()

    jobID = uuid.uuid4()
    refDate = datetime.now()

    historyData = dict()
    historyData['customerID'] = g['customerID']
    historyData['visitDate'] = refDate
    historyData['jobID'] = jobID

    result = database.addNewCustomer(historyData=historyData)
    if result is False:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype='application/json')

    else:
        payload = dict()
        payload['UUID'] = g['UUID']
        payload['queryDate'] = refDate
        payload['data'] = historyData
        return Response(dumps(payload), status=200, mimetype='application/json')