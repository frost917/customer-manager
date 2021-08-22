import psycopg2 as db
import os
# TODO 얘도 가능하면 함수 다 분리해놓을 것

class PostgresControll:
    def __init__(self):
        # DB HOST
        host = os.getenv("DB_HOST")
        database = os.getenv("DB_DATABASE")
        # DB_PORT 환경변수가 없는 경우 기본값 5432 부여
        port = 5432 if os.getenv("DB_PORT") is None else os.getenv("DB_PORT")

        # DB USER
        user = os.getenv("DB_USER")
        passwd = os.getenv("DB_PASSWD")
        try:
            self.dbconn = db.connect(
                database=database, 
                host=host, 
                port=port, 
                user=user, 
                passwd=passwd)
            self.dbconn.autocommit = True
            self.cur = self.dbconn.cursor()
        except db.DatabaseError as err:
            print(err)

    # customer table
    from customerTableQuery import getCustomerTuple, getCustomerID, addNewCustomer 

    # login

    # 로그인용 쿼리
    def getUserPasswd(self, userID):
        try:
            self.cur.execute("""
                SELECT passwd 
                FROM login
                WHERE userID = %s""",
                (userID,))
            return self.cur.fetchone()
        except db.DatabaseError as err:
            print(err)
            return None

    # UUID 불러오기
    def getUUID(self, userID, passwd):
        try:
            self.cur.execute("""
                SELECT UUID 
                FROM login
                WHERE user_id = %s, passwd = %s""",
                (userID, passwd,))
            return self.cur.fetchone()
        except db.DatabaseError as err:
            print(err)
            return None

    # visit_history table
    from visitHistoryTableQuery import getVisitHistoryTuple, getVisitHistory, addNewVisited 

    # job_list table
    from jobListTableQuery import getJobHistory, getJobsSpecipic, getJobsTuple

    # # 모든 예약 불러오기
    # def getReserveTuple(self, UUID):
    #     try:
    #         self.cur.execute("""
    #             SELECT 
    #             SELECT customerID, reservedTime
    #             FROM reserve
    #             where UUID = %s""",
    #             (UUID,))
    #     except db.DatabaseError as err:
    #         print(err)

    # # 특정 손님의 예약 불러오기
    # def getReserveSpecipic(self, UUID):
    #     try:
    #         self.cur.execute("""
    #             SELECT customerID, reservedTime
    #             FROM reserve
    #             where UUID = %s""",
    #             (UUID,))
    #     except db.DatabaseError as err:
    #         print(err)