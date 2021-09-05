import json

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
from flask import Blueprint, Response, g
from postgres.databaseConnection import PostgresControll

manager = Blueprint('getAllJobHistory', __name__, url_prefix='/jobs')

@manager.route('/', methods=['GET'])
@tokenVerify
@dataParsing
def getAllJobHistory():
    database = PostgresControll()

    result = database.getJobsDict(UUID=g['UUID'])
    if result is None:
        from msg.jsonMsg import databaseIsGone
        return Response(databaseIsGone(), status=500, mimetype='application/json',content_type='application/json')

    return Response(json.dumps(result), status=200, mimetype='application/json', content_type='application/json')
