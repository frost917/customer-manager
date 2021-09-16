from dataCheck import customerDataCheck, jobDataCheck
import json

from flask import Blueprint, Response
from postgres.databaseConnection import PostgresControll

from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing

manager = Blueprint('getJobHistory', __name__, url_prefix='/jobs')

# 특정 작업 id의 데이터를 불러옴
@manager.route('/job/<jobID>', methods=['GET'])
@tokenVerify
@customerDataCheck
@jobDataCheck
def getJobHistory(jobID):
    database = PostgresControll()

    jobData = database.getJobHistory(jobID=jobID)

    return Response(json.dumps(payload), status=200, content_type="application/json; charset=UTF-8")

