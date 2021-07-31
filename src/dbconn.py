import psycopg2 as db
import os

class Database:
    def __init__(self):
        # DB HOST
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_DATABASE")
        # DB_PORT 환경변수가 없는 경우 기본값 5432 부여
        port = 0
        port = os.getenv("DB_PORT") if os.getenv("DB_PORT") is not None else port = 5432

        # DB USER
        user = os.getenv("DB_USER")
        passwd = os.getenv("DB_PASSWD")
        try:
            self.dbconn = db.connect(database=database, host=host, port=port, user=user, passwd=passwd)
            self.dbconn.autocommit = True
            self.cur = self.dbconn.cursor()
        except db.DatabaseError as err:
            print(err)

    # 고객 명단 불러오기
    def getCustomerTuple(self, uuid):
        try:
            self.cur.execute("""
                SELECT name,phoneNumber 
                FROM customer
                WHERE uuid = %s""",
                (uuid,))
            return self.cur.fetchall()
        except db.DatabaseError as err:
            print(err)

    # 고객 UUID 불러오기
    def getCustomerID(self, uuid, name):
        try:
            self.cur.execute("""
                SELECT customerID 
                FROM customer
                WHERE uuid = %s AND name = %s""",
                (uuid, name,))
            return self.cur.fetchone()
        except db.DatabaseError as err:
            print(err)

    # 모든 작업 내역 불러오기
    def getJobsTuple(self, uuid):
        try:
            self.cur.execute("""
                SELECT jobID, jobs
                FROM jobs_list
                where uuid = %s""",
                (uuid,))
        except db.DatabaseError as err:
            print(err)

    # 특정 손님의 작업 내역 불러오기
    def getJobsSpecipic(self, uuid, customerID):
        try:
            self.cur.execute("""
                SELECT jobID, jobs
                FROM jobs_list
                where uuid = %s AND customerID = %s""",
                (uuid, customerID,))
        except db.DatabaseError as err:
            print(err)
    
    # 작업 기록 불러오기
    def getJobHistory(self, jobID):
        try:
            self.cur.execute("""
                SELECT jobHistory
                FROM misc
                where jobID = %s""",
                (jobID,))
        except db.DatabaseError as err:
            print(err)

    # 모든 예약 불러오기
    def getReserveTuple(self, uuid):
        try:
            self.cur.execute("""
                SELECT customerID, reservedTime
                FROM reserve
                where uuid = %s""",
                (uuid,))
        except db.DatabaseError as err:
            print(err)

    # 특정 손님의 예약 불러오기
    def getReserveSpecipic(self, customerID, uuid):
        try:
            self.cur.execute("""
                SELECT customerID, reservedTime
                FROM reserve
                where uuid = %s""",
                (uuid,))
        except db.DatabaseError as err:
            print(err)