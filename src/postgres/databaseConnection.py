import psycopg2
import psycopg2.extras
import os
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
            self.dbconn = psycopg2.connect(
                database=database, 
                host=host, 
                port=port, 
                user=user, 
                passwd=passwd)
            self.dbconn.autocommit = True
            self.cur = self.dbconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except psycopg2.DatabaseError as err:
            print(err)

    # customer table
    from customerTableQuery import getCustomerDict, getCustomerID, addNewCustomer
    # customer info
    from customerTableQuery import getCustomerInfo, updateCustomerInfo, deleteCustomerInfo

    # login table
    from loginTableQuery import getUserPasswd, getUUID

    # visit_history table
    from visitHistoryTableQuery import getVisitHistoryDict, getVisitHistory, addNewVisited 

    # job_list table
    from jobListTableQuery import getJobHistory, getJobsSpecipic, getJobsDict

    # # 모든 예약 불러오기
    # def getReserveDict(self, UUID):
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