from flask import Blueprint, g, Response
from auth.flaskAuthVerify import tokenVerify
from dataProcess import dataParsing
import uuid

from postgres.databaseConnection import PostgresControll

manager = Blueprint('addJobHistory', __name__, url_prefix='/jobs')

@manager.route('/', methods=['POST'])
@tokenVerify
@dataParsing
def addJobHistory():
    # 받아오는 데이터: 손님 id, 작업 비용, 작업 기록, 작업 목록
    # 생성 후 반환하는 데이터: 작업 id, 방문 날짜, 작업 id

    g['jobData']
    database = PostgresControll()

    